O código em python basicamente faz a função principal do projeto, capturando imagem, lendo as placas, conexão com database, geração de log e abrindo o servomotor ligado no arduino.
O código do arduino apenas recebe um retorno do código e dependendo do retorna executa funções de abrir e fechar a cancela, portanto é necessário rodar ambos ao mesmo tempo.
A estrutura do banco de dados é nosso banco de dados inteiro incluindo as pessoas presentes nele (apenas para teste). Esse banco de dados é um banco local, portanto não está na nuvem,
está sendo utilizado o WampServer para instanciar o banco de dados localmente para que apartir do código em python ocorra uma conexão com o mesmo e subsequente as comparações com saídas.
