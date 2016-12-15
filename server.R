# package (which generally comes preloaded).
library(datasets)

# Define a server for the Shiny app
function(input, output) {
  
  # Fill in the spot we created for a plot
  output$OLXPlot <- renderPlot({
    
    # Render a barplot
    barplot(dane.csv$V3[1:input$max], dane.csv$V1[1:input$max], 
            names.arg=dane.csv$V1[1:input$max],
            las=2,
            ylab="Liczba wyswietlen",
            xlab="")
  })
}
