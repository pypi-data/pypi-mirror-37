#########################################################################################
`brasil.gov.newfieldcomplement: Suporte a novos campos dexterity na busca multifacetada.`
#########################################################################################

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Complementa a inclusão de novos campos nos tipos de conteúdo Dexterity,
provida pelo pacote plone.app.contenttypes.

Engloba:

- Formulário de criação de novo índice e metadado no portal_catalog.
  Esse índice poderá ser utilizado nos filtros da pesquisa facetada
  (eea.facetednavigation) e na exibição do resultado da pesquisa.

- Formulário de gerenciamento de quinze listas de valores/opções, convertidas
  em quinze vocabulários dinâmicos que podem ser utilizados tanto pelos novos
  campos (seleção/checkbox) criados nos tipos de conteúdo Dexterity, quanto nos
  filtros da pesquisa facetada.

- Nova visão de pasta Facetada Tabular para exibição do resultado da pesquisa
  facetada no formato tabular de até cinco colunas.

- Novo formulário de configuração da visão Facetada Tabular, que permite a
  seleção do campo, vocabulário (caso necessário) e do título de cada uma das
  cinco colunas que podem ser exibidas no resultado da pesquisa.

- Vocabulário fixo de Estados e caminho das pastas, úteis em novos campos ou
  filtros da pesquisa facetada.


Instalação
------------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.newfieldcomplement`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.newfieldcomplement

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**Suporte a novos campos dexterity na busca multifacetada (brasil.gov.newfieldcomplement)**.

Obs.: Os sites que utilizam o pacote IDG já vem com os pacotes
**Tipos de conteúdo Dexterity (plone.app.dexterity)** e **Content-Types (plone.app.contenttypes)**
instalados. Para os sites que não utilizam o pacote IDG, é necessário que os mesmos sejam instalados.
Caso não estejam disponíveis para instalação, devem ser adicionados ao buildout:

        [buildout]
            ...
            eggs =
                plone.app.dexterity

                plone.app.contenttypes

                brasil.gov.newfieldcomplement


Documentação
--------------

.. _docs:  ./docs/README.rst

A documentação encontra-se na pasta docs_.

