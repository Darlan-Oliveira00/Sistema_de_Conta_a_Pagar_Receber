// Obter dados do usuário logado (cliente ou fornecedor)
function obterClienteLogado() {
    const usuario = localStorage.getItem('usuario');
    return usuario ? usuario : null;
}

// Obter tipo de usuário (cliente ou fornecedor)
function obterTipoUsuario() {
    return localStorage.getItem('tipoUsuario');
}

// Verificar se usuário está logado
function estaLogado() {
    return localStorage.getItem('usuario') !== null;
}

function verificarLogin() {
    if (estaLogado()) {
        renderizarLayout();
        return true;
    } else {
        renderizarPagina('login');
        return false;
    }
}

function logout() {

    localStorage.removeItem('usuario');
    localStorage.removeItem('tipoUsuario');

    renderizarPagina('login');
}

// Obter nome do usuário
function obterNomeUsuario() {
    const usuario = obterClienteLogado();
    return usuario ? usuario : 'Usuário';
}