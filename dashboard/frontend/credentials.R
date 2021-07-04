credentials = data.frame(
  username_id = c("cn_user1", "cn_user2", "annalena", "freddy"),
  passod   = sapply(c("forelle9", "thunfisch2", "forelle4", "hering"),password_store),
  permission  = c("admin", "admin", "admin", "admin"), 
  stringsAsFactors = F
)