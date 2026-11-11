// admin.js - CRUD de jogos: GET, POST, PUT e DELETE via fetch.

let todosGeneros = [];   // gêneros vindos da API (GET /api/generos)

const formJogo = document.querySelector("#form-jogo");
const botaoCancelar = document.querySelector("#btn-cancelar");

// ---------- Gêneros (checkboxes criados a partir da API) ----------
// idsMarcados: ids que devem aparecer marcados (usado na edição)
function montarGeneros(idsMarcados) {
  const area = document.querySelector("#generos");
  area.innerHTML = "";
  todosGeneros.forEach(function (genero) {
    const rotulo = document.createElement("label");
    const caixa = document.createElement("input");
    caixa.setAttribute("type", "checkbox");
    caixa.setAttribute("name", "generos");
    caixa.setAttribute("value", genero.id);
    for (let i = 0; i < idsMarcados.length; i++) {
      if (idsMarcados[i] === genero.id) {
        caixa.setAttribute("checked", "checked");
      }
    }
    const texto = document.createElement("span");
    texto.textContent = genero.nome;
    rotulo.appendChild(caixa);
    rotulo.appendChild(texto);
    area.appendChild(rotulo);
  });
}

async function carregarGeneros() {
  try {
    const resposta = await fetch(API_URL + "/generos");
    const generos = await resposta.json();
    if (generos.erro) {
      mostrarMensagem(generos.erro, "erro");
      return;
    }
    todosGeneros = generos;
    montarGeneros([]);
  } catch (erro) {
    mostrarMensagem("Não foi possível conectar à API. Verifique se o Flask está rodando.", "erro");
  }
}

// ---------- READ: lista de jogos ----------
async function listarJogos() {
  const tabela = document.querySelector("#tabela-jogos");
  try {
    const resposta = await fetch(API_URL + "/jogos");
    const jogos = await resposta.json();
    if (jogos.erro) {
      mostrarMensagem(jogos.erro, "erro");
      return;
    }
    tabela.innerHTML = "";
    jogos.forEach(function (jogo) {
      tabela.appendChild(criarLinha(jogo));
    });
  } catch (erro) {
    mostrarMensagem("Não foi possível conectar à API. Verifique se o Flask está rodando.", "erro");
  }
}

function criarLinha(jogo) {
  const linha = document.createElement("tr");

  let nomes = "";
  for (let i = 0; i < jogo.generos.length; i++) {
    if (i > 0) {
      nomes = nomes + ", ";
    }
    nomes = nomes + jogo.generos[i].nome;
  }

  const valores = [jogo.titulo, jogo.desenvolvedora, jogo.ano_lancamento, nomes];
  valores.forEach(function (valor) {
    const celula = document.createElement("td");
    celula.textContent = valor;
    linha.appendChild(celula);
  });

  const celulaAcoes = document.createElement("td");
  const acoes = document.createElement("div");
  acoes.classList.add("acoes");

  // O botão Editar é um link para #painel-form: assim a tela rola até o formulário
  const botaoEditar = document.createElement("a");
  botaoEditar.classList.add("botao", "botao-secundario", "botao-pequeno");
  botaoEditar.setAttribute("href", "#painel-form");
  botaoEditar.textContent = "Editar";
  botaoEditar.addEventListener("click", function () {
    editarJogo(jogo);
  });

  const botaoExcluir = document.createElement("button");
  botaoExcluir.classList.add("botao", "botao-perigo", "botao-pequeno");
  botaoExcluir.setAttribute("type", "button");
  botaoExcluir.textContent = "Excluir";
  botaoExcluir.addEventListener("click", function () {
    if (confirm("Excluir o jogo " + jogo.titulo + "?")) {
      excluirJogo(jogo.id);
    }
  });

  acoes.appendChild(botaoEditar);
  acoes.appendChild(botaoExcluir);
  celulaAcoes.appendChild(acoes);
  linha.appendChild(celulaAcoes);
  return linha;
}

// ---------- Formulário: preencher (editar) e limpar ----------
function editarJogo(jogo) {
  document.querySelector("#jogo-id").value = jogo.id;
  document.querySelector("#titulo").value = jogo.titulo;
  document.querySelector("#desenvolvedora").value = jogo.desenvolvedora;
  document.querySelector("#ano").value = jogo.ano_lancamento;
  document.querySelector("#imagem").value = jogo.imagem;
  document.querySelector("#descricao").value = jogo.descricao;

  const ids = [];
  jogo.generos.forEach(function (genero) {
    ids.push(genero.id);
  });
  montarGeneros(ids);

  document.querySelector("#titulo-form").textContent = "Editar jogo";
  botaoCancelar.classList.remove("oculto");
  mostrarMensagem("Editando " + jogo.titulo + ". Altere os campos e clique em Salvar jogo.", "info");
}

function limparFormulario() {
  document.querySelector("#jogo-id").value = "";
  document.querySelector("#titulo").value = "";
  document.querySelector("#desenvolvedora").value = "";
  document.querySelector("#ano").value = "";
  document.querySelector("#imagem").value = "";
  document.querySelector("#descricao").value = "";
  montarGeneros([]);
  document.querySelector("#titulo-form").textContent = "Cadastrar novo jogo";
  botaoCancelar.classList.add("oculto");
}

botaoCancelar.addEventListener("click", function () {
  limparFormulario();
  limparMensagem();
});

// ---------- CREATE (POST) e UPDATE (PUT) ----------
formJogo.addEventListener("submit", async function (evento) {
  // ATENÇÃO (exceção às apostilas): preventDefault() não aparece nas apostilas de DWS.
  // Sem ele a página recarregaria ao enviar e o fetch seria cancelado.
  evento.preventDefault();

  // Gêneros marcados (seletor CSS com :checked, via querySelectorAll)
  const idsGeneros = [];
  document.querySelectorAll("#generos input:checked").forEach(function (caixa) {
    idsGeneros.push(Number(caixa.value));
  });
  if (idsGeneros.length === 0) {
    mostrarMensagem("Marque pelo menos um gênero.", "erro");
    return;
  }

  const dados = {
    titulo: document.querySelector("#titulo").value,
    desenvolvedora: document.querySelector("#desenvolvedora").value,
    ano_lancamento: Number(document.querySelector("#ano").value),
    descricao: document.querySelector("#descricao").value,
    imagem: document.querySelector("#imagem").value,
    generos: idsGeneros,
  };

  // Campo oculto vazio = cadastro novo (POST). Com id = edição (PUT).
  const id = document.querySelector("#jogo-id").value;
  let url = API_URL + "/jogos";
  let metodo = "POST";
  if (id !== "") {
    url = url + "/" + id;
    metodo = "PUT";
  }

  mostrarMensagem("Salvando...", "info");
  try {
    const resposta = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });
    const resultado = await resposta.json();
    if (resultado.erro) {
      mostrarMensagem(resultado.erro, "erro");
      return;
    }
    if (metodo === "POST") {
      mostrarMensagem("Jogo cadastrado com sucesso!", "sucesso");
    } else {
      mostrarMensagem("Jogo atualizado com sucesso!", "sucesso");
    }
    limparFormulario();
    await listarJogos();   // sempre atualiza a lista depois de POST/PUT/DELETE
  } catch (erro) {
    mostrarMensagem("Não foi possível conectar à API. Verifique se o Flask está rodando.", "erro");
  }
});

// ---------- DELETE ----------
async function excluirJogo(id) {
  mostrarMensagem("Excluindo...", "info");
  try {
    const resposta = await fetch(API_URL + "/jogos/" + id, { method: "DELETE" });
    const resultado = await resposta.json();
    if (resultado.erro) {
      mostrarMensagem(resultado.erro, "erro");
      return;
    }
    mostrarMensagem(resultado.mensagem, "sucesso");
    await listarJogos();
  } catch (erro) {
    mostrarMensagem("Não foi possível conectar à API. Verifique se o Flask está rodando.", "erro");
  }
}

// ---------- Início ----------
carregarGeneros();
listarJogos();
