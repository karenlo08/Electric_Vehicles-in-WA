import pandas as pd
import plotly.graph_objects as go
mapbox_access_token = 'pk.eyJ1Ijoia2FyZW52YXJnYXNseXUwOCIsImEiOiJjazRubnRxbXIwdWpxM21xeXV4OHFjc3N0In0.FVcUnql3bnxVxNyBRnaZmw'

df2017 = pd.read_csv('documents/ev2/top1_2017_ev.csv')
df2018 = pd.read_csv('documents/ev2/top1_2018_ev.csv')

def prepare_source_to_plot(df):
    d = {0:'red',1:'yellow',5:'blue',2:'purple',21:'orange',
         6 :'gold',3:'magenta',9:'pink', 22:'fuchsia', 26:'gray', 15:'brown'}
    
    arr = df['Make_decode'].map(d)
    df = df[['lat','lon']]    
   
    return df,arr

def plot_with_animation(df,arr):
    data = [go.Scattermapbox(
               lat=[47.6062],
               lon=[-122.3321],
               mode='markers',
               #marker=dict(size=10, color='red')
               marker=dict(size=10, color=arr)
            )
        ]

    layout = go.Layout(width=800,
    autosize=True,
    hovermode='closest',
    mapbox=dict(accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(lat=47.6062,
                            lon=-122.3321),
                pitch=0,
                zoom=9,
                style='light'
                )
            )


    lats = list(df['lat'])
    lons = list(df['lon'])

    frames = [dict(data= [dict(type='scattermapbox',
                           lat=lats[:k+1],
                           lon=lons[:k+1])],
               traces= [0],
               name='frame{}'.format(k)       
              )for k  in  range(1, len(df))]           
    sliders = [dict(steps= [dict(method= 'animate',
                           args= [[ 'frame{}'.format(k) ],
                                  dict(mode= 'immediate',
                                  frame= dict( duration=0, redraw= True ),
                                           transition=dict( duration= 0)
                                          )
                                    ],
                            label='{:d}'.format(k)
                             ) for k in range(len(df))], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Point: ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0)
           ]
    layout.update(updatemenus=[dict(type='buttons', showactive=False,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=0, 
                                                                    redraw=True),
                                                         transition=dict(duration=0),
                                                         fromcurrent=True,
                                                         mode='immediate'
                                                        )
                                                   ]
                                             )
                                        ]
                               )
                          ],
              sliders=sliders);
    fig=go.Figure(data=data, layout=layout, frames=frames)
    import plotly.io as pio
    pio.renderers.default = "browser"  ##offline plot
    fig.show()
    
    
def main():
    df, arr = prepare_source_to_plot(df2017)
    df2, arr2 = prepare_source_to_plot(df2018)
    plot_with_animation(df,arr)
    plot_with_animation(df2,arr2)


if __name__ == '__main__':
    main()
    


