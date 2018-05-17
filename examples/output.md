```puml
package mynetwork {
  component ubuntu_desktop [ubuntu_desktop
  ---
  ports:8080:8080,5900:5900,
  aliases:ubuntu_desktop.com,
  ]
  component gitlab_chprot [gitlab_chprot
  ---
  ports:443:443,22:22,7080:80,
  aliases:gitlab.com,
  ]
  component swagger_ui [swagger_ui
  ---
  ports:6080:80,
  aliases:swagger_ui.com,
  ]
}

[ubuntu_desktop] --> [gitlab_chprot]
[ubuntu_desktop] --> [swagger_ui]

cloud Repository {
  [ubuntu_desktop] --> [uphy/ubuntu_desktop_jp:16.04]
  [gitlab_chprot] --> [gitlab/gitlab_ce:latest]
  [swagger_ui] --> [schickling/swagger_ui]
}
```