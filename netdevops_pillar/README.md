# NETDEVOPS DEMO

## Usando el codigo

1. Actualiza el achivo de inventario con los datos que se te proveen en el sandbox de Devnet. Ejemplo:

    CSR1000v credentials: 10.10.20.30 [SSH:admin/Cisco123]
    IOS credentials: 10.10.20.35 [Telnet: admin/Cisco123]
    Nexus 9K credentials: 10.10.20.40 [SSH:admin/RG!_Yw200]
    Devbox credentials: 10.10.20.50 [SSH:developer/C1sco12345]


```inventory 
[controller]
controller ansible_host=10.10.20.50 ansible_user=developer ansible_ssh_pass=C1sco12345 ansible_sudo_pass=C1sco12345

[iosxe]
csr ansible_host=10.10.20.30 ansible_user=admin ansible_ssh_pass=Cisco123

[iosxr]
xr ansible_host=10.10.20.35 ansible_user=admin ansible_ssh_pass=Cisco123

[nxos]
n9k ansible_host=10.10.20.40 ansible_user=admin ansible_ssh_pass=RG!_Yw200

```

1. Instalar las librerias requeridas:
``` 
ansible-galaxy collection install -r requirements.yml
```
3. Correr los playbooks:
``` 
ansible-playbook playbook/docker.yml
ansible-playbook playbook/telemetria.yml
ansible-playbook playbook/restauracion.yml
```

a. Las imagenes del stack de Telemetria TIG (no tls and tls) se pueden encontrar aqui:
https://hub.docker.com/repository/docker/sarifern/tig-stack-tls