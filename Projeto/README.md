# BagulhoRank
Escolha entre dois Bagulhos e o app atualizará o BagulhoScore™ para ambos (aumentar ou diminuir a depender da escolha).

## Telas
- Tela A: escolha entre dois Bagulhos exibidos aleatoriamente.
- Tela B: adicione ou remova Bagulhos e veja a sua lista de Bagulhos, ordenada do maior para o menor BagulhoScore™.

## Modelos
- Modelo 1: Bagulho (nome, Categoria, imagem, bagulho_score).
- Modelo 2: Categoria (nome, cor).

Relação entre os dois modelos:
- one-to-many (uma Categoria possui vários Bagulhos, mas cada Bagulho só pode pertencer a uma Categoria).
> Sim, eu sei que isso não faz sentido, mas quem cria as regras aqui sou eu! >:)

## Operações Básicas (CRUD)
- Create: adicionar um Bagulho a sua lista.
- Read: ler dois Bagulhos aleatórios da sua lista e exibi-los na Tela A.
- Update: atualizar o BagulhoScore™ dos dois Bagulhos exibidos na Tela A com base na escolha feita.
- Delete: excluir um Bagulho da sua lista.

## Opções Implementadas
- Paginação com "scroll infinito", para a Tela B.
