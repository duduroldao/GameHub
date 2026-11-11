// detalhes.js - mostra um jogo. O id chega pela URL: detalhes.html?id=3

async function carregarDetalhes() {
  // ATENÇÃO (exceção às apostilas): URLSearchParams e window.location.search
  // não aparecem nas apostilas de DWS. São a única forma de ler "?id=3" no JavaScript.
  const parametros = new URLSearchParams(window.location.search);
  const id = parametros.get("id");

  if (id === null || id === "") {
    mostrarMensagem("Nenhum jogo foi escolhido. Volte ao catálogo e clique em Ver detalhes.", "erro");
    return;
  }

  mostrarMensagem("Carregando jogo...", "info");
  try {
    const resposta = await fetch(API_URL + "/jogos/" + id);
    const jogo = await resposta.json();
    if (jogo.erro) {
      mostrarMensagem(jogo.erro, "erro");
      return;
    }

    document.querySelector("#det-imagem").setAttribute("src", "../img/jogos/" + jogo.imagem);
    document.querySelector("#det-imagem").setAttribute("alt", "Capa de " + jogo.titulo);
    document.querySelector("#det-titulo").textContent = jogo.titulo;
    document.querySelector("#det-desenvolvedora").textContent = jogo.desenvolvedora;
    document.querySelector("#det-ano").textContent = jogo.ano_lancamento;
    document.querySelector("#det-descricao").textContent = jogo.descricao;

    const areaGeneros = document.querySelector("#det-generos");
    areaGeneros.innerHTML = "";
    jogo.generos.forEach(function (genero) {
      const etiqueta = document.createElement("span");
      etiqueta.classList.add("etiqueta");
      etiqueta.textContent = genero.nome;
      areaGeneros.appendChild(etiqueta);
    });

    document.querySelector("#detalhe").classList.remove("oculto");
    limparMensagem();
  } catch (erro) {
    mostrarMensagem("Não foi possível carregar o jogo. Confira o endereço e se o Flask está rodando.", "erro");
  }
}

carregarDetalhes();
