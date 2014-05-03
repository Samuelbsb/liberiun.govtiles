*****************
liberiun.govtiles
*****************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

Este pacote contem alguns tiles desenvolvidos pela Liberiun
para serem usados nos portais do Governo Federal.

Estado deste pacote
-------------------

O **liberiun.govtiles** está estável e atualmente é usado nos portais da Ouvidoria e do PPA.

.. image:: https://travis-ci.org/liberiun/liberiun.govtiles.png?branch=master
	:target: https://travis-ci.org/liberiun/liberiun.govtiles

.. image:: https://coveralls.io/repos/liberiun/liberiun.govtiles/badge.png
	:target: https://coveralls.io/r/liberiun/liberiun.govtiles

Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``liberiun.govtiles`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            liberiun.govtiles

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Instale o produto por meio do painel de controle na opção **Complementos**.