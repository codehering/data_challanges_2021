observe({ 
  if (USER$login == FALSE) {
    if (!is.null(input$login)) {
      if (input$login > 0) {
        Username <- isolate(input$userName)
        Password <- isolate(input$passwd)
        if(length(which(credentials$username_id==Username))==1) { 
          pasmatch  <- credentials["passod"][which(credentials$username_id==Username),]
          pasverify <- password_verify(pasmatch, Password)
          if(pasverify) {
            USER$login <- TRUE
          } else {
            shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade")
            shinyjs::delay(3000, shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade"))
          }
        } else {
          shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade")
          shinyjs::delay(3000, shinyjs::toggle(id = "nomatch", anim = TRUE, time = 1, animType = "fade"))
        }
      } 
    }
  }    
})
