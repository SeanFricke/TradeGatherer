import panel as pn
import controller

control = controller.Controller()
result = control.show()

pn.serve(result)
