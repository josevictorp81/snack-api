# snack-api

Esta é uma aplicação que auxilia no gerenciamento de pedidos de lanches, onde o cenário abordado é uma escola. Esta, permite que os usuários/responsáveis por um aluno, gerenciem os pedidos de lanches para o mesmo, e para tais ações, esta _API_ disponiliza os seguites recursos:

```
- Cadastro de usuário
- Login de usuário
- Ver as informações do seu perfíl

- Cadastrar o/os filhos(as)
- Listar o/os filhos(as)

- Listar lanches disponíveis
- Listar as turmas da escola

- Cadastrar um pedido
- Listar os pedidos que ja foram feitos
- Listar um pedidos específico
- Editar um pedido
- Deletar um pedido
```

Para mais detalhes sobre os endpoints, acessar a rota `/` ou `/redoc`.

# Executar

Comandos para exectar api usando docker.

-   Criar imagen docker

```
docker-compose build
```

-   Fazer as migrations

```
docker-compose run --rm api python manage.py makemigrations
docker-compose run --rm api python manage.py migrate
```

-   Criar super usuário

```
docker-compose run api --rm python manage.py createsuperuser
```

-   Executar testes

```
docker-compose run api --rm python manage.py test
```

-   Iniciar execução da API

```
docker-compose up
```

-   Encerrar execução da API

```
docker-compose down
```

## Tecnologias

-   <a href='https://www.djangoproject.com/' target='_blank'>Django</a>
-   <a href='https://www.django-rest-framework.org/' target='_blank'>Django Rest Framework</a>
-   <a href='https://docs.docker.com/' target='_blank'>Docker</a>
-   <a href='https://docs.docker.com/compose/' target='_blank'>Docker Compose</a>
