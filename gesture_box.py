from kivy.gesture import GestureDatabase
from kivy.uix.boxlayout import BoxLayout
from kivy.gesture import Gesture

gesture_strings = {
    'left_to_right_line': 'eNq1mE1y3DYQhfe8iLXRFPofuICyTZUOkFLsKVllR5qSxkl8+zS7ZWWaFYfYaDajeQQf8PUDAVBXD18e/vx+uD++nL89H5dfXr9Pbbn6dILl9sPj3R/HD8sJ/U//ouXl9sPL+fnpy/HFf/Jy9fUky9V/mtxGs+Wkq5X5/aenh8fzeltfbxs/ue3XtdVyghzBOoTvfgvgctMOrQFpgz6odeEm1Nfx/L1ep+Xmuh2MGzJAM8HBXWV5+f3u/7vh6EaW+5/3cP/DvHU1Q0W2gebtd80DHSzNr+3AQm0gNGC3aXS8bvKvvWqXJm1oEzBk3bfvYT8m7QmVrI1GgJ3Jdu0xEkCYtG/aAQEVeus89iuPGPY0Zy8ioAjDBmjX1vftI1iUOXseStTfEoCJ6kS2aO/mH+HiZLiso1kfnYFJWPftKcKlyXAZGoqwsBFYh0H7/pEu0bv5R7w0GS+JzxkRVC+NDb931z7SJXsv+wiXJsMlAJRh0vvwpaftLwwc4fJkuL4aNP/YayPYLz5HuDwZLjLSIOjWjTxb3F8aOMLlyXCxIfo1BGZFvz4x/kiX7d38I16ejNcfWRrGAxuxNBu79hLxCryXfaQrk+m+7bU4RFHH/tIjka5Mpuvbiu+2zafoMCXfBfb9I12ZTNc3WzHxChHjMLS+//RKxCuT8b5NHEH0rdcmFjeNgHUmYPf3w8IAMFITtS77y4NGwEpz9uzLjwJZb6aGfT9fjXxV5uxNwfXmxy1jJtzf2DXiVZuyh8a9DViH7se53vZnj0a4OubsyY9UPvFxLcx6wNq1t4jW5qIFVWnYzISHL6Iz9hGtzUULozeVgb65+PFkYuJbJGtzySIOXxO88MqjC1lMnPXt4ePz8fj49i5gur4M+NWrG6ZDW24Yzb/OJ+vLnWtatLFqCpdab6FJ0WDVxqufpoarBtCLSCEiF5FDJC2ihGhYRF1FhNqRhUhwGJcfu2gRaGj1tmDzel6KI+B8aSpi0NGPMryKgUejFTHwuDKPwPNdoYiBx1J7DzzupToj8AS898uPXrQIPMHaQeAJFy9owedHv6oGoBhUNQilb9pSqqOqwehTsqqS0werGpSKG9VSlaoGmtJmZDktqTpATsw6jQCCTbk6AKZqVaVUKxsk26ZmkGyyaZts2qqabFqrA8mmG99k00qBybZJCJPNas0w2ayyYbL1OjJMtr7xTba+8U22vvFNtrHxTbZR2TDZRnWgZBu9qsFmrfoSplrHS5Rq7Y041U1vkmrNjYLNYNObpVpzo57qpreRaq0Zt1QrGycb1DFwstXH2E+TqdbeONmwzhJONqzEnGy46S3ZNs8QJxttxpBsVNkk2TbPmyQbVWJJNqpjkGTjWnU/r97l1vX5+HD/+bz+t8lPrzdr5i7+9fDp/Dk0XwJzLrl6fvp6fL57/HiMKxbb7aq/bqy/nZ6fPn37mF7dO/NXYD9kNfa5I92P6utWf/gHjU3d+Q==',
    'right_to_left_line': 'eNq1WMty4zYQvPNHrMuqMC8M8APea6r8ASnHZtmq3dgqWZtk/z6DASWStijwIl5kjhqNQfcAGHmz+7H75/f2pf84/jr03ffhcx+6zfMeuoe7t8e/+7tuj/anfVD38XD3cTy8/+g/7JW7zc+9dJuLJA8O6/axUKmN37/v3o5lWCrD8sKwPwqq20PNoKTw24YAdvffwjZA5BgwJ2UEUkUuCf1XANTdh23ElCkk0AghRMv2r8frs7DPIt3LlQleKrdkyQCZc0wixNom95WDriKfZy5t8uTkeRU5FM7zBNgkRxcfYQ05qw7hRJE1t8nRyWkVOQcUEEVCDczQ1gXdUVzlKOVZ7im22d1S1Buxu6c49RSUiYaiQCEY2XlSi5LbnpJ7SnAbcveUJp6GTImTuxaQo+iZHDPEyaPcZndPaeJp0ICRSr2ZxDHlUXWksRZd/ja7e0p6I3b3lAZPeZuBBDEA2n40ZfpvQc7skM5ulL2a20cMu6kMN2J3V3lwtQjDGiNArJOksWBswvMmtR1L7Yph95Rl5M6cSlacGG0f4Zh4mDDbWSDtQ4DdUtbbkLujnM/kwBisZlJ0YVRGWUJ5G4WxHdFkF3dU4Ebs7qiMjkIUSRIzJKRs5xgN7H4+KGaRQbQo7fNL3FORVewRIdRvUs7Ull3cU9FV5Dl7zsMCsF3q4qZKvg17dFMjrGEHwsHrso9lxW0d3dS4ylSIg+Dq6q9hd1PjKlPt0oAJf0xtdnc1arPcjR35dLpJ+b5dMtFNjRNTIVkPkVKQQDCjFp2J3qRWd1RHR4OCXXNDRWcuwp7Jp9SauL1N1R3VycGLHKxxG7LMdmWd2WluaWg3veqOqrQvjULPw/6v1e6il98AT4e+fzt39BpLS6/abe4NuA3dPbF9TJ/YHfeauseCgGVEdkTURUQKFUHLCHCEpGUEVsQVDnIE8zKCHUGyjBBH4LIe1hMWRLiSqRaEtWDLCNdU9EqmrqlIqAja5unDhsiuqWCuiLIkC7qMEuQz3hCxIlxGu1nrsFyDrpx1jR4UqEEXiyl+zs4QVBEuFkM1XoYUXB/K6RT8mrnrQ5qXEa4PDfVyEeH61PwvI6xpcgjxFYjLRUhXIK4XAV6BuHoUaCoDBJcPc6xR/uoxBKkQuAJxNe00qhAcuLVGeR5NNYrzaK7RMItCmEVhiLoeqHkexRpN8yjVKJ8K6aswUCU4HR0XIVWCmKblaN1qjco8WlcdYR6tq5ZPDHXVpulsTp1AsEogOBuIVYLTxjtFqwTldfrQFELLkHTBWazi8JD3RYiJU4/u13738nr0/6nY/oP5cZDKz9SHu393z8dXh9gqGYsvFj2+/+wPj29PvX+TvPEv8eGa+XN/eH/+9VSpsyVivQyj1YUSkV1f3uRt/wdC4ZmI',
	'bottom_to_top_line': 'eNq1mN1u40YMhe/1IslNDf4OyRfw3hbIAxRpYiTBbhMj9rbdty81I0t2YtWLFewbO6PDbyieEWeU25evL3//WD1tdvvv75vuy/C9he72cYvd3c3r/V+bm25L+TO/uNvd3ez2729fN7v8U7rbb1vtbs9C7qqs25YeZRm/fXt53fdh3ofFTNjvvarbYsugT+FHhiB1699gVRAIUQGYQUrUdP7tL3O3hhWwADuzCIuHWXS7P+//fxaps2j3NEygBu5a1AqzC2C3e/pldr1xtIlNbgpOBY2xaCxhe2XHyBZVQ0N0BoswXsCmWnnCq7Cpsnlkc/GShS6lEBUQXASvZpJeB17dJLsOvNpJk52UK4TJxYsomPrEzkEC1hJQHMxML8K5+sl4HXg1lPk68GooT4YSnK7Eo5oTORBbsHlKwn+CXh1luxK9WsqTpcgqQRxBef/GoRM9O1opQsJEyo5OF+lSPRW8Er2aKnwlenVVJlfBrWdGtnZHCJeJDrmYQtQh233+LnKZXl2VyVXQPtJIQSK7u8pR8od9hEph9fTXLvOrrzL5ClkWL+ZIFJypHvD9JSAxVwwJy26RD8XldaPVWZ2cBYgsUIA4ZTxmWzme4HRP6ZfsJX71Vgdv+/SPFraZl+P8040smKt5OKHQT+CruaojPstK5qSa9SHLLrqIXs1VG+nZXANMsrhJQj+hs6GI5ebFnk06K3qRXq3VONCx7dMebf8jX0Qv1diCI12P9gjVXLGL6NXWMtqKeYABZeXSDkwLc6+ultHV3PFyyaO2viBL6dXVMrpKalYy79wiIk2lZa6W6moZXSXPQMnnKR+XwHzyF9Gtumqjq6f9ajwr/SK8mmqjqcyRlTfAwGKES1OvptpoKhcs2cmQgLLjIF1ckP2rwMP7ZvM6Huyt9Cd7s+52LRh9f50+pVuj4Aq6/da8u59TSFPErEJlFccfS7nDrNygAh1nFVGaguYUWfMzU3KTWwavs/1+jEqFNIV+Brq2KbUpPgWvGeJ0SunlpcrB+yn5Y1JVYU1Rk8oXmDOKVnrQj5fWLHxGHgd5D9RmX8DJYLuXaAUGaYPeBul4MIv0aYJoZQRuimhhcjxoZ24jWuUAP9+GNzujzCqCm8LmFALw2c7weXk5I49ZObb5EWBWQjhIcFbCMEhoXhKDhGcleqDIrKQccpmtudiBUuYlh1zmq+4ySOYr7TZI5qsbQ7o4X90YKJjVbX3sefPy9Lzv/5HQ98J8SUlBDv/z8rh/rqPct5ITlxGll+zfvm3e718fNlUmde/tx4ee+8f2/e3x+0NDaz76K8++nbOA5w4RUU+0q/8AAJ5q8g=='
}

from kivy.uix.boxlayout import BoxLayout

#This database can compare gestures the user makes to its stored     gestures
#and tell us if the user input matches any of them.
gestures = GestureDatabase()
for name, gesture_string in gesture_strings.items():
    gesture = gestures.str_to_gesture(gesture_string)
    gesture.name = name
    gestures.add_gesture(gesture)

class GestureBox(BoxLayout):

    def __init__(self, **kwargs):
        for name in gesture_strings:
            self.register_event_type('on_{}'.format(name))
        super(GestureBox, self).__init__(**kwargs)

    def on_left_to_right_line(self):
        pass
    def on_right_to_left_line(self):
        pass
    def on_bottom_to_top_line(self):
        pass

#To recognize a gesture, you’ll need to start recording each individual event in the
#touch_down handler, add the data points for each call to touch_move , and then do the
#gesture calculations when all data points have been received in the touch_up handler.

    def on_touch_down(self, touch):
        #create an user defined variable and add the touch coordinates
        touch.ud['gesture_path'] = [(touch.x, touch.y)]
        super(GestureBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        touch.ud['gesture_path'].append((touch.x, touch.y))
        super(GestureBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if 'gesture_path' in touch.ud:
            #create a gesture object
            gesture = Gesture()
            #add the movement coordinates
            gesture.add_stroke(touch.ud['gesture_path'])
            #normalize so thwu willtolerate size variations
            gesture.normalize()
            #minscore to be attained for a match to be true
            match = gestures.find(gesture, minscore=0.3)
            if match:
                print("{} happened".format(match[1].name))
                self.dispatch('on_{}'.format(match[1].name))
        super(GestureBox, self).on_touch_up(touch)