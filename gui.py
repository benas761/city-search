import PySimpleGUI as sg
from objectiveFunctions.binary import binary
from objectiveFunctions.proportional import paretoProportional, partiallyProportional, proportional

from searchAlgorithms import brute, random

def drawWindow():
  sg.theme('default1')
  searchMap = {
    'brute': brute,
    'random': random
  }
  objectiveMap = {
    'binary': binary,
    'proportional': proportional,
    'partiallyProportional': partiallyProportional,
    'paretoProportional': paretoProportional
  }

  def layout(optionColumn):
    return [ 
      [
        sg.Column(
          optionColumn + [[sg.Button('Ok'), sg.Button('Quit')]]
        )
      ]
    ]

  optionColumn = [
    [ sg.Check('Precalculate distances', default=True, key='noDistances') ],
    [
      sg.Text('Objective function: ', size=24), 
      sg.DropDown(
        list(objectiveMap.keys()), 
        default_value=list(objectiveMap.keys())[0], 
        key='objective',
        size=30
      ) 
    ],
    [
      sg.Text('Expanding firm index (-1 if the firm is new): ', size=31), 
      sg.Input('-1', key='expandingFirm', size=24) 
    ],
    [
      sg.Text('Minimum attraction: ', size=24), 
      sg.Input('0.2', key='minAttraction', size=32) 
    ],
    [
      sg.Text('Location data file: ', size=24), 
      sg.Input('data/demands_LT_50.dat', key='points', size=32)
    ],
    [
      sg.Text('Competitor data file: ', size=24), 
      sg.Input('data/competitors_4.dat', key='competitors', size=32)
    ],
    [
      sg.Text('Potential new object location file: ', size=24), 
      sg.Input('data/potentialLocations_12.dat', key='candidates', size=32)
    ],
    [
      sg.Text('New object count: ', size=24), 
      sg.Input('3', key='newCount', size=32)
    ],
    [
      sg.Text('Logging level: ', size=24), 
      sg.DropDown(
        ['debug', 'info', 'warning', 'error', 'critical'],
        default_value='info', 
        key='loggingLevel',
        size=30
      ) 
    ],
    [
      sg.Text('Search algorithm: ', size=24),
      sg.DropDown(
        list(searchMap.keys()), 
        default_value=list(searchMap.keys())[0], 
        key='search',
        size=30, 
        enable_events=True
      )
    ],
    # Optional subparser arguments
    [
      sg.Text('Number of loops: ', key='cyclesTitle', size=24, visible=False),
      sg.Input('1000', key='cycles', size=32, visible=False)
    ]
  ]

  window = sg.Window('Window Title', layout(optionColumn), finalize=True)

  # Display and interact with the Window
  args = None
  while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
      break
    if event == 'Ok':
      args = values
      args['objective'] = objectiveMap[args['objective']]
      args['search'] = searchMap[args['search']]
      args['minAttraction'] = float(args['minAttraction'])
      args['expandingFirm'] = int(args['expandingFirm'])
      args['newCount'] = int(args['newCount'])
      if 'cycles' in args.keys(): args['cycles'] = int(args['cycles'])
      break
    if event == 'search':
      window['cyclesTitle'].Update(visible=False)
      window['cycles'].Update(visible=False)
      # add some extra variables from subparsers
      if values['search'] == 'random':
        window['cyclesTitle'].Update(visible=True)
        window['cycles'].Update(visible=True)
  window.close()
  return args