function paginaCadastroItens() {
  return `
    <div class="container-item">
      <h1>Cadastro de itens</h1>

      <form id="form-cadastro-item">
        <div>
          <label>Tipo de item</label>
          <input type="text" id="item-tipo" placeholder="Produto/Serviço" required>
        </div>

        <div>
          <label>Descrição do item:</label>
          <input type="text" id="item-descricao" placeholder="Informe a descrição do item" required>
        </div>

        <div>
          <label>Nome do item:</label>
          <input type="text" id="item-nome" placeholder="Informe o nome do item" required>
        </div>

        <div>
          <label>Valor de Custo:</label>
          <input type="number" id="item-valorBruto" placeholder="Informe o valor de custo" step="0.01" required>
        </div>

        <div>
          <label>Valor final:</label>
          <input type="number" id="item-valorFinal" placeholder="Digite o valor final" step="0.01" required>
        </div>

        <div class="btn-area">
          <button type="button" id="btn-cadastroItem" onclick="cadastrarItem()">Cadastrar</button>
        </div>
      </form>
      
      <div id="footer-cadastroItens">
        <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
      </div>
    </div>
  `
}

async function cadastrarItem() {
  const tipo = document.getElementById('item-tipo').value.trim();
  const descricao = document.getElementById('item-descricao').value.trim();
  const nome = document.getElementById('item-nome').value.trim();
  const valorBruto = document.getElementById('item-valorBruto').value.trim();
  const valorFinal = document.getElementById('item-valorFinal').value.trim();

  if (!tipo || !descricao || !nome || !valorBruto || !valorFinal) {
    alert('Preencha todos os campos obrigatórios');
    return;
  }

  if (isNaN(valorBruto) || isNaN(valorFinal)) {
    alert('Informe valores numéricos válidos');
    return;
  }

  const valorBrutoNum = parseFloat(valorBruto);
  const valorFinalNum = parseFloat(valorFinal);

  if (valorBrutoNum <= 0 || valorFinalNum <= 0) {
    alert('Os valores devem ser maiores que zero');
    return;
  }

  try {
    const rota = obterTipoUsuario();
    const cpfCnpj = obterCfpCnpjUsuario();
    console.log(cpfCnpj);

    const dados = {
      classificacao_produto_servico: tipo,
      nome_produto_servico: nome,
      detalhes_produto_servico: descricao,
      valor_final_de_venda_produto_servico: valorFinalNum
    };

    if (rota === 'cliente') {
      dados.cpf = cpfCnpj;
      dados.valor_custo_de_venda_produto_servico = valorBrutoNum;
    } else {
      dados.cnpj = cpfCnpj;
      dados.valor_custo_produto_servico = valorBrutoNum;
    }

    const btnCadastrar = document.getElementById('btn-cadastroItem');
    btnCadastrar.disabled = true;
    btnCadastrar.textContent = "Cadastrando...";

    const response = await fetch(`${API_BASE_URL}/produto_servico_${rota}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dados)
    });

    if (response.ok) {
      const item = await response.json();
      console.log('Item cadastrado com sucesso:', item);

      alert(`✓ Item "${nome}" cadastrado com sucesso!`);


    } else {
      const erro = await response.json();
      console.error('Erro da API:', erro);
      alert(`Erro ao cadastrar: ${erro.detail || 'Erro desconhecido'}`);
    }

  } catch (error) {
    console.error('Erro na requisição:', error);
    alert(`Erro ao conectar ao servidor: ${error.message}`);
  }
}