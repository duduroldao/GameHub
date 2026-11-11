// catalogo.js - lista todos os jogos vindos da API (GET /api/jogos).

async function carregarCatalogo() {
  const lista = document.querySelector("#lista-jogos");
  mostrarMensagem("Carregando jogos...", "info");
  try {
    const resposta = await fetch(API_URL + "/jogos");
    const jogos = await resposta.json();
    if (jogos.erro) {
      mostrarMensagem(jogos.erro, "erro");
      return;
    }
    lista.innerHTML = "";
    if (jogos.length === 0) {
      mostrarMensagem("Nenhum jogo cadastrado ainda.", "info");
      return;
    }
    jogos.forEach(function (jogo) {
      lista.appendChild(criarCardJogo(jogo, "../img/jogos/", "detalhes.html"));
    });
    document.querySelector("#total").textContent = jogos.length + " jogos no catálogo. Escolha um para ver os detalhes.";
    limparMensagem();
  } catch (erro) {
    mostrarMensagem("Não foi possível conectar à API. Verifique se o Flask está rodando.", "erro");
  }
}

carregarCatalogo();
