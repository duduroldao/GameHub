# GameHub – Catálogo Digital de Jogos

## O que é o GameHub?

O GameHub é um site criado para funcionar como um catálogo de jogos eletrônicos. Nele, é possível encontrar diferentes jogos, visualizar suas capas e conhecer informações como desenvolvedora, ano de lançamento, descrição e gênero. A ideia é reunir essas informações em um só lugar, de uma forma simples e organizada.

## Objetivo

O objetivo do projeto é colocar em prática os conteúdos aprendidos nas aulas de Desenvolvimento de Websites, Programação Orientada a Objetos e Banco de Dados. Através do GameHub, buscamos desenvolver um sistema que reúna criação de páginas web, programação em Python e armazenamento de informações em um banco de dados.

## Como funciona?

O site possui uma página inicial, um catálogo de jogos, uma página com os detalhes de cada título e uma área administrativa. No catálogo, o visitante pode consultar os jogos disponíveis e acessar suas informações. Já na área administrativa, é possível cadastrar novos jogos, editar os dados existentes, visualizar os registros e excluir jogos.

As informações são armazenadas no MySQL. Quando o usuário acessa o catálogo ou realiza alguma alteração na área administrativa, o JavaScript envia as solicitações para o back-end, desenvolvido em Python com Flask, que realiza as operações necessárias no banco de dados.

## Tecnologias utilizadas

Para desenvolver o GameHub, utilizamos HTML e CSS na criação e organização das páginas, JavaScript para as interações e comunicação com o servidor, Python e Flask para o funcionamento do back-end e MySQL para armazenar as informações dos jogos e seus gêneros.

## Banco de dados

O banco de dados possui três tabelas principais: jogos, generos e jogo_genero. A primeira armazena os dados dos jogos, a segunda guarda os gêneros disponíveis e a terceira faz a ligação entre eles. Essa organização permite que um jogo tenha vários gêneros e que um mesmo gênero esteja associado a diferentes jogos.

## Considerações finais

O desenvolvimento do GameHub permite reunir em um único projeto os conhecimentos trabalhados durante o curso. Além da criação do site, também trabalhamos com banco de dados, programação orientada a objetos e comunicação entre o front-end e o back-end, entendendo melhor como essas partes funcionam juntas.