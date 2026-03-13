# BagulhoRank
Escolha entre dois Bagulhos e o app atualizará a sua nota para ambos (aumentar ou diminuir a depender da escolha).

## Telas
- Tela 1: escolha entre dois Bagulhos exibidos aleatoriamente.
- Tela 2: veja a sua lista de Bagulhos, ordenada da maior para a menor nota.

## Modelos
- Modelo 1: Bagulho (nome, nota, Categoria).
- Modelo 2: Categoria (nome).

Relação entre os dois modelos:
- one-to-many (uma Categoria possui vários Bagulhos, mas cada Bagulho só pode pertencer a uma Categoria).
> Sim, eu sei que isso não faz sentido, mas quem cria as regras aqui sou eu! >:)

## Operações Básicas (CRUD)
- Create: adicionar um Bagulho a sua lista.
- Read: ler dois Bagulhos aleatórios da sua lista e exibi-los na Tela 1.
- Update: atualizar a nota dos dois Bagulhos exibidos com base na escolha feita.
- Delete: excluir um Bagulho da sua lista.

## Opções Implementadas
- Paginação com "scroll infinito", para a Tela 2.
