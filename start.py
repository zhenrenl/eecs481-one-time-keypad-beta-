from controller import app
import controller
import threading

p = threading.Thread(target=controller.monitor)
p.start()
app.run()