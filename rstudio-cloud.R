# TODO: 
# - usethis-like function to put bash export-command into clipboard
# - document these functions

get_dash_url <- function(absolute) {
  rstudioapi::translateLocalUrl("https://localhost:8050", absolute = absolute)
}

cloud_env_var <- function() {
  paste0("/", get_dash_url(FALSE))
}

browse_dash_app <- function() {
  get_dash_url(TRUE) |> browseURL()
}

view_dash_app <- function() {
  get_dash_url(TRUE) |> rstudioapi::viewer()
}