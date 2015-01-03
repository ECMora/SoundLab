- Copiar la carpeta "styles" para la raíz de la aplicación (donde está "Models.pyw")
- Revisar el código que está en "Models.pyw" que acompaña este "readme", y copiar las
  3 secciones enmarcadas entre los comentarios: "### fm-code-start:..." y
  "### fm-code-end:...", en posiciones similares a como están ahora. Las secciones
  son:
  1) Creación del menú para los estilos. Va en inmediatamente después de la
     definición del resto del menú en Container.__init__(...)
      ### fm-code-start: Menu for styles ###
      vMenu = menu.addMenu("View")
      sSubMenu = vMenu.addMenu("Styles")
      sSubMenu.addAction("Default", self.ChangeStyle)
      sSubMenu.addAction("Coffee", self.ChangeStyle)
      sSubMenu.addAction("Classic", self.ChangeStyle)
      self.setMenuBar(menu)
      ### fm-code-end: Menu for styles ###
  2) Definicion del handler para los cambios de estilos. Va en cualquier lugar
     dentro de la clase Container (ahora está inmediatamente después del __init__)
      ### fm-code-start: Handler (slot) for changing styles ###
      def ChangeStyle(self):
        selectedStyle = self.sender().text()
        if (selectedStyle == "Coffee"):
          qss = QFile("styles/coffee.qss")
        elif (selectedStyle == "Classic"):
          qss = QFile("styles/classic.qss")
        else:
          qss = QFile("styles/default.qss")
        qss.open(QIODevice.ReadOnly | QIODevice.Text)
        app.setStyleSheet(QString(qss.readAll()))
        qss.close()
      ### fm-code-end: Handler (slot) for changing styles ###
  3) Aplicación del estilo por defecto. Va antes de la instrucción de ejecutar la
     aplicación: app.exec_().
      ### fm-code-start: Applying default style ###
      from styles import default_img
      qss = QFile("styles/default.qss")
      qss.open(QIODevice.ReadOnly | QIODevice.Text)
      app.setStyleSheet(QString(qss.readAll()))
      qss.close()
      ### fm-code-end: Applying default style ###
