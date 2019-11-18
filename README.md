# Contexto

Temos diversos freelancers, cada freelancer possui experiencias profissionais descritas nos seus perfis.

Nós usamos essas experiencias profissionais no nosso algorítimo de busca para o freelancer com mais relevância para nossa missão.

Vocês pode achar um exemplo da missão e o modelo de um freelancer na pasta `/examples`.

# Exercício

No nosso algorítimo de busca nós usamos o total de meses de experiencia em cada habilidade do freelancer.

Se vocês abrir o arquivo `example/freelancer.json`, você verá que esse freelancer tem 3 experiencias profissionais, você também notará que ele utiliza Javascript desde a sua primeira experiencia profissional, em maio de 2013 ele continuou a utilizar Javascript até a sua última experiencia em maio de 2018.

Nós gostaríamos de computar o **total de meses** que o freelancer trabalhou com **cada habilidade**

Você irá receber um payload similar a `example/freelancer.json`.

O resultado deverá ser formatado em JSON com a exata mesma estrutura do exemplo a seguir:
```json
{
    "freelance": {
        "id": 42,
        "computedSkills": [
            {
                "id": 241,
                "name": "React",
                "durationInMonths": 28
            },
            {
                "id": 270,
                "name": "Node.js",
                "durationInMonths": 28
            },
            {
                "id": 370,
                "name": "Javascript",
                "durationInMonths": 60
            },
            {
                "id": 400,
                "name": "Java",
                "durationInMonths": 40
            },
            {
                "id": 470,
                "name": "MySQL",
                "durationInMonths": 32
            }
        ]
    }
}
```

# Regras

1. Meses que as experiências se sobrepõe não devem ser contabilizadas duas vezes, veja [assets/months-overlap.png](./assets/months-overlap.png)
2. Todas os valores de `startDate` e `endDate` serão sempre o primeiro dia do mês.
3. Sua aplicação deve ser uma API rest
4. Você deve usar Python 3.6+
5. Pode usar qualquer biblioteca que desejar
6. Se houver um erro no payload de entrada retorne 422
7. A duração em meses deve ser arredondada

# O que é avaliado

1. Estrutura e clareza do código
2. Resolução do problema
3. Documentação
4. Testes
5. Uso inteligente de pacotes ou bibliotecas externas
6. Respeito pelo principio KISS e DRY
7. Uso de git commits

# Extra
1. Docker

# Como

1. Dê um fork nesse repositório ou clone, caso não possua uma conta no github
2. Faça o exercício
3. Abra uma pull request para esse repositório ou nos envie um arquivo com o seu código.