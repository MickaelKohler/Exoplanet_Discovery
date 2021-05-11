import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def load_df(url):
    df = pd.read_csv(url)
    return df

# option
st.set_page_config(page_title="Exoplanet Discovery",
                   page_icon="🧊 ",
                   layout="wide",
                   initial_sidebar_state="expanded")


#############
## sidebar ##
############# 

st.sidebar.title('Exoplanet Discovery')
st.sidebar.subheader('Navigation')

categorie = st.sidebar.radio("Categories", ("Accueil", "Observer les Exoplanètes", "Les Exoplanètes habitables", "L'IA à l'aide des Astrophysicien"))

st.sidebar.title(' ')
option = st.sidebar.beta_expander("Options")
option.markdown(
    """
    L'option _Montre moi la data_ affichera les données 
    qui ont permis de réaliser les graphiques, sous forme de tableaux. 
    """)
show = option.checkbox('Montre moi la data')

expander = st.sidebar.beta_expander("Sources")
expander.markdown(
    """
    __Les bases des données utilisées__ : 

    [NASA Exoplanet Archives](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS) : 
    Data brutes sur les exoplanètes et leur système solaire.

    [Planetary Habitability Laboratory](http://phl.upr.edu/projects/habitable-exoplanets-catalog/data/database) : 
    Détermine quelles sont les exoplanètes habitables ou inhabitables.
    """)
expander.info('Résiliation des **Pirates Ducks** : _Antoine, Franck, Michaël, Mickaël_')
expander.info('Hackathon organisé par la **WildCodeSchool** le 12/05/2021')


##########
## DATA ##
##########

# modifier selon la localisation de la BD
phl_db = 'http://www.hpcf.upr.edu/~abel/phl/hec2/database/phl_exoplanet_catalog.csv'
nea_db = 'https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/planets.csv'

planets = load_df(nea_db)
plan_hab = load_df(phl_db)


###############
## MAIN PAGE ##
###############

if categorie == 'Accueil':
    st.title('Exoplanet Discovery')
    st.subheader('Donner de la vie à la data')
    st.title(" ")

    st.markdown(
        """
        
        """
    )




elif categorie == "Observer les Exoplanètes":
    st.title('Comment découvrir des Exoplanètes')
    st.subheader('Des outils et des hommes')
    st.title(" ")

    st.markdown("""
    
    __La découverte d'un nouveau Monde__
    
    Le 6 octobre 1995, les astronomes Michel Mayor et Didier Queloz, ont annoncés la découverte d'une première exoplanète.
    Cette planète, nommée __51 Pegasi B__, se  situe à une cinquantaine d'années lumière de la Terre dans la constelation du Pégase.

    """)

    fig = px.histogram(planets, 
    x = "disc_year" ,
    color = "discoverymethod",
    title= "Le nombre de planètes découvertes par années et par méthodes",
    color_discrete_sequence= px.colors.sequential.Plasma_r,
    nbins = 10)  
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    
    __Qu'est ce que la méthode des vitesses radiales__

    La force de gravité des planètes modifie le déplacement de leur étoile.
    Les capteurs situés sur Terre vont détécter des spéctres passant d'une couleur bleu à une couleur rouge. 
    Le décalage de temps durant le changement de couleurs permet de déduire des paramètres physiques comme la vitesse, la masse et la distance.
    
    __Et la méthode la méthode du transit ?__

    Cette méthode consiste en l'observation d'une répétition constante d'une __variation de luminosité__ d'une étoile.
    Lorsqu'une planète passe devant une étoiles, elle crée une zone d'ombre qui font varier la luminosité captée depuis la Terre.

    """)

    fig = px.scatter(
        data_frame = planets,
         x = "sy_disterr1" , y = "pl_orbper",
         title = "Les méthodes utilisées en fonction de la période orbitale et de la distance à la Terre", 
         color = 'discoverymethod' 
     )
    fig.update_layout(
        xaxis_title = "Distance à la Terre (al)",
        yaxis_title = "Période orbitale autour de l'étoile"
     )
    fig.update_xaxes(
        range=[-2, 200]
     )
    fig.update_yaxes(
        range=[0, 200]
    )
    st.plotly_chart(fig, use_container_width=True) 

    
elif categorie == "Les Exoplanètes habitables":
    st.title('Les caractéristiques des Exoplanètes habitables')
    st.subheader('Où sont elles et quels sont leurs projets')
    
    phl_sample = plan_hab[['P_NAME', 'S_TYPE_TEMP', 'P_TYPE', 'S_AGE', 'P_DISTANCE', 'S_TEMPERATURE']]
    zone_hab = pd.merge(planets, phl_sample, left_on='pl_name', right_on='P_NAME', how='left')
    habit = zone_hab[zone_hab['P_HABITABLE'].isin([1, 2])]

    st.markdown(
        """
        On dénombre dans la base de données plus de *** exoplanètes et seulement *** qui sont considérées comme pouvant potentiellement habriter la vie.
        """
    )

    # réparition des planetes
    constelation = planets[planets['P_HABITABLE'].isin([1, 2])][['pl_name', 'hostname', 'S_CONSTELLATION']]
    constelation.dropna(inplace=True)
    fig =px.sunburst(
        constelation,
        path=['S_CONSTELLATION', 'hostname', 'pl_name'],
        maxdepth=2,
        color_discrete_sequence= px.colors.sequential.Peach_r
    )
    fig.update_layout(
        title="<b>Où sont localisées les planètes habitables ?</b>",
        margin = dict(l=10, r=10, b=10, t=30)
    )
    st.plotly_chart(fig, use_container_width=True)

    planet_name = habit[habit.index == habit['sy_dist'].idxmin()].iloc[0,0]
    planet_distance = (habit['sy_dist'].min()*3.26156).round(2)
    st.markdown(
        f"""
        __Où se situe la planète la plus proche ?__ La planète potentiellement habitables la plus proche est __{planet_name}__, 
        qui est située à {planet_distance} années lumières.

        A savoir, qu'il faudait _76 624 993 ans_ de voyage à la sonde _Voyager 1_ pour atteindre cette exoplanète.
        
        Pour qu'une planète soit considéré comme habitable, elle doit être située dans la __Zone Habitable__ qui est la région de l’espace 
        où les conditions sont favorables à l’apparition de la vie, telle que nous la connaissons sur Terre.

        Les limites des zones habitables sont calculées à partir des éléments connus de la biosphère de la Terre, 
        comme sa position dans le Système solaire et la quantité d'énergie qu'elle reçoit du Soleil.  
        
        Le graphique ci-dessous permet de bien percevoir cette _Zone Habitable_, les exoplanètes devant s'éloigner à mesure que 
        son étoile gagne en puissance.       
        """
    )

    # zone habitable
    clean_zone = zone_hab[(zone_hab['P_DISTANCE'] < 2) & (zone_hab['S_TEMPERATURE'] > 2500) & (zone_hab['S_TEMPERATURE'] < 8000)]
    clean_zone['P_HABITABLE'] = clean_zone['P_HABITABLE'].apply(lambda x: 'Non Habitable' if x == 0 else 'Habitable')
    inHab = clean_zone[clean_zone['P_HABITABLE'] == 'Non Habitable']
    hab = clean_zone[clean_zone['P_HABITABLE'] == 'Habitable']

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            text=inHab['pl_name'],
            mode='markers',
            x=inHab['P_DISTANCE'],
            y=inHab['S_TEMPERATURE'],
            marker=dict(
                color='coral',
                opacity=0.3,
            ),
            name='Non Habitable'
        )
    )
    fig.add_trace(
        go.Scatter(
            text=hab['pl_name'],
            mode='markers',
            x=hab['P_DISTANCE'],
            y=hab['S_TEMPERATURE'],
            marker=dict(
                color='darkgreen'
            ),
            name='Habitable'
        )
    )
    fig.update_layout(
        title='<b>La situation des planètes habitables selon la chaleur du soleil et la distance</b>',
        yaxis=dict(title="Température du soleil (en kelvins)"),
        xaxis=dict(title="Distance planète/étoile (en année-lumière)"),
        margin = dict(l=10, r=10, b=10, t=70))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # Comparatif Habitable/inhabitable
    st.subheader("Qu'est ce qui caractérise une planète habitable ?")
    st.markdown(
        """
        La _Zone Habitable_ met en avant la nécessité de déterminer les critères 
        qui font qu’une exoplanète soit suspectée comme pouvant être habitable. 

        On peut donc tenter de comparer les caractéristiques des exoplanètes 
        considérées comme habitables de l’ensemble des exoplanètes.

        Restons dans les étoiles et essayons de répondre à la question : 
        _Quelle type d’étoile favorise la présence d’exoplanètes habitables ?_
        """
    )

    # Sun Type
    sType = pd.DataFrame(zone_hab['S_TYPE_TEMP'].value_counts(normalize=True)*100).rename(columns={'S_TYPE_TEMP':'Exoplanètes'})
    sType_hab = habit['S_TYPE_TEMP'].value_counts(normalize=True)*100
    sType_tab = pd.concat([sType, sType_hab], axis=1).reindex(index = ['O','B','A', 'F', 'G', 'K', 'M'])
    sType_tab = sType_tab.fillna(0).rename(columns={'S_TYPE_TEMP':'Habitables'}).round(2)

    fig = px.bar(sType_tab, x=sType_tab.index, y=["Exoplanètes", "Habitables"],
                title="<b>La répartition des exoplanètes selon le type de leur Soleil</b> (en pourcents)", barmode='group')
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=True, font_family='IBM Plex Sans',
                      xaxis=dict(title="Catégorie d'étoile"),
                      yaxis=dict(title=None),
                      uniformtext_minsize=10, uniformtext_mode='hide',
                      margin=dict(l=10, r=10, b=10),
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(
                            x=0,
                            y=1,
                            traceorder="normal",
                            bgcolor='rgba(0,0,0,0)',
                            font=dict(
                                size=12)))
    texts = [sType_tab["Exoplanètes"], sType_tab["Habitables"]]
    for i, t in enumerate(texts):
        fig.data[i].text = t
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.beta_columns([1,2])
    with col1:
        st.markdown(
            """
            On peut constater que ce sont surtout les étoiles de type K et M qui comprennent le plus d’exoplanètes habitables. 
            Ce qui s’explique sans doute par le faite que ce sont les plus petites et donc les moins chaudes. 

            Le tableau ci-contre explique la différence entre chaque type.
            """)

    with col2:
        sol_typ = pd.DataFrame(data=[['> 25 000 K', 'bleue', 'azote, carbone, hélium et oxygène'],
                                     ['10 000–25 000 K', 'bleue-blanche', 'hélium, hydrogène'],
                                     ['7 500–10 000 K', 'blanche', 'hydrogène'],
                                     ['6 000–7 500 K', 'jaune-blanche', 'métaux : fer, titane, calcium, strontium et magnésium'],
                                     ['5 000–6 000 K', 'jaune (comme le Soleil)', 'calcium, hélium, hydrogène et métaux'],
                                     ['3 500–5 000 K', 'orange', 'métaux et monoxyde de titane'],
                                     ['< 3 500 K', 'rouge', 'métaux et monoxyde de titane']],
                               index=['O', 'B', 'A', 'F', 'G', 'K', 'M'],
                               columns=['température', 'couleur conventionnelle', "raies d'absorption"])
        st.write(sol_typ)
    
    # Sun Age
    sAge = planets.groupby((zone_hab['S_AGE'] // 2) * 2).count()[['pl_name']]
    sAge.iloc[5, 0] = sAge.iloc[5:, 0].sum()
    sAge['norm'] = ((sAge['pl_name']*100) / sAge['pl_name'].sum()).round(2)
    sAge = sAge.drop(columns=['pl_name']).drop([12, 14]).rename(columns={'norm':'Exoplanètes'})

    sAge_hab = habit.groupby((habit['S_AGE'] // 2) * 2).count()[['pl_name']]
    sAge_hab['norm'] = ((sAge_hab['pl_name']*100) / sAge_hab['pl_name'].sum()).round(2)
    sAge_hab = sAge_hab.drop(columns=['pl_name']).rename(columns={'norm':'Habitables'})

    sAge_tab = pd.concat([sAge, sAge_hab], axis=1).fillna(0).round(2)
    sAge_tab.rename(index={0:'<2', 2:'2-4', 4:'4-6', 6:'6-8', 8:'8-10', 10:'+10'}, inplace=True)

    fig = px.bar(sAge_tab, x=sAge_tab.index, y=["Exoplanètes", "Habitables"],
                title="<b>La répartition des exoplanètes selon l'age de leur étoile</b> (en pourcents)", barmode='group')
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=True, font_family='IBM Plex Sans',
                      xaxis=dict(title="Age de l'étoile (Gy)"),
                      yaxis=dict(title=None),
                        uniformtext_minsize=10, uniformtext_mode='hide',
                        margin=dict(l=10, r=10, b=10),
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(
                            x=0,
                            y=1,
                            traceorder="normal",
                            bgcolor='rgba(0,0,0,0)',
                            font=dict(
                                size=12)))
    texts = [sAge_tab["Exoplanètes"], sAge_tab["Habitables"]]
    for i, t in enumerate(texts):
        fig.data[i].text = t
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        Toujours dans les étoiles, on remarque que les exoplanètes observées sont essentiellement situées 
        sur les __étoiles les plus jeunes__, même si aucune tranche d’âge ne sort du lot. 

        Pour que la vie puisse apparaître sur une planète, il ne suffit pas qu'elle soit dans l'écosphère de son étoile ; 
        son système planétaire doit se situer __assez près du centre de la galaxie__ pour avoir suffisamment d'éléments lourds 
        qui favorisent la formation de planètes telluriques et des atomes nécessaires à la vie (fer, cuivre, etc).

        Mais ce système devra également se situer __assez loin du centre galactique__ pour éviter des dangers tels que 
        le trou noir au centre de la galaxie et les supernova.

        Mais l'exoplanète en elle même doit présenter des conditions intrinsèque pour 
        être une bonne candidate pour accueillir la vie. 
        """
    )

    # Exoplanet type
    pType = pd.DataFrame(zone_hab['P_TYPE'].value_counts(normalize=True)*100).rename(columns={'P_TYPE':'Exoplanètes'})
    pType_hab = habit['P_TYPE'].value_counts(normalize=True)*100
    pType_tab = pd.concat([pType, pType_hab], axis=1).reindex(index = ['Miniterran','Subterran','Terran', 'Superterran', 'Neptunian', 'Jovian'])
    pType_tab = pType_tab.fillna(0).round(2).rename(columns={'P_TYPE':'Habitables'})

    fig = px.bar(pType_tab, x=pType_tab.index, y=["Exoplanètes", "Habitables"],
                title="<b>La répartition des exoplanètes selon leur type</b> (en pourcents)", barmode='group')
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=True, font_family='IBM Plex Sans',
                      xaxis=dict(title="Type d'exoplanète"),
                      yaxis=dict(title=None),
                        uniformtext_minsize=10, uniformtext_mode='hide',
                        margin=dict(l=10, r=10, b=10),
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(
                            x=0,
                            y=1,
                            traceorder="normal",
                            bgcolor='rgba(0,0,0,0)',
                            font=dict(
                                size=12)))
    texts = [pType_tab["Exoplanètes"], pType_tab["Habitables"]]
    for i, t in enumerate(texts):
        fig.data[i].text = t

    col1, col2 = st.beta_columns([3, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.title(" ")
        st.markdown(
            """
            Les type d'exoplanet selon
            la masse de la terre (MT): 
            - _Miniterran_ : -0,1 MT
            - _Subterran_ : 0,1 à 0,5 MT
            - _Terran_ : 0,5 à 2 MT
            - _Superterran : 2 à 10 MT
            - _Neptunian_ : 10 à 50 MT
            - _Jovian_ : +50 MT 
            """
        )
    
    st.markdown(
        """
        Les exoplanète habitables sont essentiellement situées sur des planètes équivalentes 
        à la terre ou légèrement plus grosse. Comme pour la _Zone Habitable_, la conditions de 
        validité pour être considérée comme une exoplanète habitable est très restreinte. 

        Ces conditions ne sont bien sur pas limitatives. Il existe de nombreux critères à prendre en compte. 
        De nombreuses variables qui peuvent être étudiées par un algorithme afin de 
        pouvoir créer un modèle permettant de repérer les exoplanètes.
        """
    )


elif categorie == "L'IA à l'aide des Astrophysicien":
    st.title("L'intelligence artificielle à la recherche de la vie")
    st.subheader("Comment le Machine Learning peut venir à l'aide des Astrophysicien")
    st.title(" ")

    col1, col2 = st.beta_columns(2)
    













    
