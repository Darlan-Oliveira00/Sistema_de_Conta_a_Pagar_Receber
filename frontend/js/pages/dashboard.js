// Exemplo em qualquer página
function paginaDashboard() {
    const cliente = obterClienteLogado();
    const nome = cliente ? cliente.nome : 'Visitante';

    return `
    <div class="dashboard">
        <h1>Bem-vindo, ${nome}!</h1>
        <p>CPF: ${cliente}</p>
        
    </div>
    `;
}