# package (which generally comes preloaded).
library(datasets)

# Use a fluid Bootstrap layout
fluidPage(    
  
  # Give the page a title
  titlePanel("Najlepsze ogloszenia OLX"),
  
  # Generate a row with a sidebar
  sidebarLayout(      
    
    # Define the sidebar with one input
    sidebarPanel(
      selectInput("max", "Liczba najlepszych:", 
                  choices=c("3","5","10", "15", "20", "25", "30")),
      hr()
    ),
    
    # Create a spot for the barplot
    mainPanel(
      plotOutput("OLXPlot")  
    )
    
  )
)
