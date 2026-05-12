// Exemplo em qualquer página
function paginaDashboard() {
    const cliente = obterClienteLogado();
    const nome = cliente ? cliente.nome : 'Visitante';

    return `
        <div class="content-dashboard">
                <h1>Bem-vindo, ${nome}!</h1>
      <div class="cards">

        <div class="card">
          <div class="icon">📈</div>

          <h2>Total de Receitas</h2>

          <div class="value">
            R$ 100.000,00
          </div>
        </div>
       
        <div class="card">
          <div class="icon red">📊</div>

          <h2>Total de Despesas</h2>

          <div class="value red">
            R$ 100.000,00
          </div>
        </div>
       
        <div class="card">
          <div class="icon">🗂</div>

          <h2>Total de produtos cadastrados</h2>

          <div class="value">
            100
          </div>
        </div>

        <div class="card">
          <div class="icon">👜</div>

          <h2>Vendas Registradas</h2>

          <div class="value">
            100
          </div>
        </div>

      </div>

    </div>
    `;
}