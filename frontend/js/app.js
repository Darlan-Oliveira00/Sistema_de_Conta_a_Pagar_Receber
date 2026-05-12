document.addEventListener('DOMContentLoaded', function () {
    verificarLogin();
});

function renderizarPagina(pagina) {
    const app = document.getElementById('app');

    switch (pagina) {
        case 'login':
            app.innerHTML = paginaLogin();
            break;
        case 'cadastroFornecedor':
            app.innerHTML = paginaCadastroFornecedor();
            break;
        case 'cadastroCliente':
            app.innerHTML = paginaCadastroCliente();
            adicionarEventoCEP();
            break;
        case 'cadastroDespesa':
            app.innerHTML = paginaCadastroDespesa();
            break;
        case 'layout':
            renderizarLayout();
            break;
        default:
            app.innerHTML = '<p>Página não encontrada</p>';
    }
}

function renderizarLayout() {
    const app = document.getElementById('app');
    app.innerHTML = paginaLayout();
    setupLayout();
}