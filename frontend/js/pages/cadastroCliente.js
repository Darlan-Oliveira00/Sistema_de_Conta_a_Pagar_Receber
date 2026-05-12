function paginaCadastroCliente(){
    return`
    <div class="card">

      <h1>Cadastro de Cliente</h1>

      <form id="formCadastroCliente">
        <div class="form-grid">

          <div class="input-group">
            <label>Nome Completo:</label>
            <input type="text" id="nome" required>
          </div>

          <div class="input-group">
            <label>CPF:</label>
            <input type="text" id="cpf" required>
          </div>

          <div class="input-group">
            <label>E-mail:</label>
            <input type="email" id="email" required>
          </div>

          <div class="input-group">
            <label>Telefone:</label>
            <input type="text" id="telefone" required>
          </div>

          <div class="input-group">
            <label>Data de Nascimento</label>
            <input type="date" id="dataNascimento" required>
          </div>

          <div class="input-group">
            <label>CEP</label>
            <input type="text" id="cep" required>
          </div>

          <div class="input-group">
            <label>Rua</label>
            <input type="text" id="logradouro" required>
          </div>

          <div class="input-group">
            <label>Bairro</label>
            <input type="text" id="bairro" required>
          </div>

          <div class="input-group">
            <label>Estado:</label>
            <input type="text" id="estado" required>
          </div>

          <div class="input-group">
            <label>Cidade:</label>
            <input type="text" id="cidade" required>
          </div>

          <div class="input-group">
            <label>Senha:</label>
            <input type="password" id="senha" required>
          </div>

          <div class="input-group">
            <label>Confirmar senha:</label>
            <input type="password" id="confirmarSenha" required>
          </div>

        </div>

        <div class="btn-area">
          <button id="btn-cadastrar" type="button" onclick="cadastrarCliente()">Cadastrar-se</button>
        </div>

      </form>

    </div>
    `
}

async function cadastrarCliente() {
    const nome = document.getElementById('nome').value;
    const cpf = document.getElementById('cpf').value.replace(/\D/g, '');
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value.replace(/\D/g, '');
    const dataNascimento = document.getElementById('dataNascimento').value;
    const cep = document.getElementById('cep').value;
    const logradouro = document.getElementById('logradouro').value;
    const bairro = document.getElementById('bairro').value;
    const estado = document.getElementById('estado').value;
    const cidade = document.getElementById('cidade').value;
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmarSenha').value;

    // Validações
    if (!nome || !cpf || !email || !telefone || !dataNascimento || !cep || !logradouro || !bairro || !estado || !cidade || !senha) {
        alert('Preencha todos os campos obrigatórios');
        return;
    }

    if (senha !== confirmarSenha) {
        alert('As senhas não conferem');
        return;
    }

    if (senha.length < 6) {
        alert('A senha deve ter no mínimo 6 caracteres');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/cliente`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nome,
                cpf,
                email,
                numero_telefone_pessoal: telefone,
                data_nascimento: dataNascimento + 'T00:00:00',
                cep,
                logradouro,
                bairro,
                estado,
                cidade,
                senha
            })
        });

        if (response.ok) {
            const cliente = await response.json();
            alert('Cadastro realizado com sucesso!');
            console.log('Cliente cadastrado:', cliente);
            renderizarPagina('login');
        } else {
            const erro = await response.json();
            alert('Erro ao cadastrar: ' + (erro.detail || 'Tente novamente'));
            console.error('Erro no cadastro:', erro);
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao conectar com o servidor');
    }
}

async function buscarCEP(cep) {
    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const dados = await response.json();

        if (dados.erro) {
            throw new Error('CEP não encontrado');
        }

        return dados;
    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
        return null;
    }
}

function adicionarEventoCEP() {
    const cepInput = document.getElementById("cep");
    
    if (cepInput) {
        cepInput.addEventListener("blur", async (e) => {
            const cep = e.target.value.replace(/\D/g, '');
            
            if (cep.length === 8) {
                const dados = await buscarCEP(cep);
                if (dados) {
                    document.getElementById("logradouro").value = dados.logradouro;
                    document.getElementById("bairro").value = dados.bairro;
                    document.getElementById('estado').value = dados.uf;
                    document.getElementById('cidade').value = dados.localidade;
                } else {
                    alert("CEP não encontrado!");
                }
            }
        });
    }
}