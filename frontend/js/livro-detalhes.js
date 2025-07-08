// frontend/js/livro-detalhes.js

class LivroDetalhes {
    constructor() {
        this.livroId = this.extrairIdLivro();
        this.instancias = [];
        this.instanciasFiltradas = [];
        this.ordenacao = 'id';
        
        this.initEventListeners();
        this.carregarDados();
    }

    extrairIdLivro() {
        const path = window.location.pathname;
        const segments = path.split('/');
        return segments[segments.length - 1];
    }

    initEventListeners() {
        const sortSelect = document.getElementById('sortInstancias');
        
        // Mudança na ordenação
        sortSelect.addEventListener('change', () => {
            this.ordenacao = sortSelect.value;
            this.ordenarInstancias();
            this.renderizarInstancias();
        });
    }

    async carregarDados() {
        try {
            this.showLoading(true);
            
            // Carregar dados do livro
            const livroResponse = await fetch(`/livros/${this.livroId}`);
            if (!livroResponse.ok) {
                throw new Error('Livro não encontrado');
            }
            const livro = await livroResponse.json();
            
            // Carregar instâncias do livro
            const instanciasResponse = await fetch(`/livros/${this.livroId}/instancias`);
            if (!instanciasResponse.ok) {
                throw new Error('Erro ao carregar instâncias');
            }
            this.instancias = await instanciasResponse.json();
            this.instanciasFiltradas = [...this.instancias];
            
            this.renderizarLivro(livro);
            this.ordenarInstancias();
            this.renderizarInstancias();
            
        } catch (error) {
            console.error('Erro:', error);
            this.mostrarErro(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    renderizarLivro(livro) {
        document.getElementById('livroTitulo').textContent = livro.titulo;
        document.getElementById('livroAutor').querySelector('span').textContent = livro.autor;
        document.getElementById('livroEditora').querySelector('span').textContent = livro.editora;
        document.getElementById('livroId').querySelector('span').textContent = livro.idLivro;
        document.getElementById('livroCutter').querySelector('span').textContent = livro.codigoCutter;
        document.getElementById('livroEstante').querySelector('span').textContent = livro.estanteId;
        
        // Atualizar título da página
        document.title = `${livro.titulo} - Detalhes | Biblioteca IoT`;
        
        document.getElementById('livroInfo').classList.remove('hidden');
    }

    ordenarInstancias() {
        this.instanciasFiltradas.sort((a, b) => {
            if (this.ordenacao === 'data') {
                return new Date(b.ultimaAtualizacao) - new Date(a.ultimaAtualizacao);
            } else {
                return a.idInstancia.localeCompare(b.idInstancia);
            }
        });
    }

    renderizarInstancias() {
        const container = document.getElementById('instanciasList');
        const countElement = document.getElementById('instanciasCount');
        
        const count = this.instanciasFiltradas.length;
        const plural = count !== 1 ? 's' : '';
        countElement.textContent = `(${count} instância${plural})`;
        
        if (this.instanciasFiltradas.length === 0) {
            container.innerHTML = this.renderNenhumaInstancia();
            document.getElementById('instanciasContainer').classList.remove('hidden');
            return;
        }

        const instanciasHtml = this.instanciasFiltradas.map(instancia => this.renderInstancia(instancia)).join('');
        container.innerHTML = instanciasHtml;
        
        document.getElementById('instanciasContainer').classList.remove('hidden');
    }

    renderInstancia(instancia) {
        const dataFormatada = this.formatarData(instancia.ultimaAtualizacao);
        const situacaoClass = this.getSituacaoClass(instancia.situacao);
        const situacaoIcon = this.getSituacaoIcon(instancia.situacao);
        
        return `
            <div class="instancia-card border border-gray-200 rounded-lg p-3 lg:p-4 hover:shadow-md transition-shadow bg-gray-50 hover:bg-white">
                <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-3 lg:space-y-0">
                    <!-- Informações principais -->
                    <div class="flex-1 space-y-2">
                        <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4">
                            <h4 class="font-semibold text-gray-900 text-sm lg:text-base font-mono">
                                <i class="fas fa-tag mr-2 text-gray-500"></i>
                                ${instancia.idInstancia}
                            </h4>
                            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${situacaoClass} mt-1 sm:mt-0">
                                <i class="fas ${situacaoIcon} mr-1"></i>
                                ${instancia.situacao.toUpperCase()}
                            </span>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 text-xs lg:text-sm text-gray-600">
                            <div class="flex items-center">
                                <i class="fas fa-map-marker-alt mr-2 text-gray-400"></i>
                                <strong>Posição X:</strong> <span class="ml-1">${instancia.posX}</span>
                            </div>
                            <div class="flex items-center">
                                <i class="fas fa-clock mr-2 text-gray-400"></i>
                                <strong>Atualizado:</strong> <span class="ml-1">${dataFormatada}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Botão Localizar -->
                    <div class="flex justify-end">
                        ${this.renderBotaoLocalizar(instancia)}
                    </div>
                </div>
            </div>
        `;
    }



    getSituacaoClass(situacao) {
        const classes = {
            'disponivel': 'bg-green-100 text-green-800',
            'emprestado': 'bg-yellow-100 text-yellow-800',
            'cativo': 'bg-red-100 text-red-800'
        };
        return classes[situacao] || 'bg-gray-100 text-gray-800';
    }

    getSituacaoIcon(situacao) {
        const icons = {
            'disponivel': 'fa-check-circle',
            'emprestado': 'fa-clock',
            'cativo': 'fa-lock'
        };
        return icons[situacao] || 'fa-question-circle';
    }

    formatarData(dataString) {
        const data = new Date(dataString);
        const agora = new Date();
        const diffMs = agora - data;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) {
            return 'Hoje';
        } else if (diffDays === 1) {
            return 'Ontem';
        } else if (diffDays < 7) {
            return `${diffDays} dias atrás`;
        } else {
            return data.toLocaleDateString('pt-BR');
        }
    }

    renderNenhumaInstancia() {
        return `
            <div class="text-center py-8 lg:py-12">
                <i class="fas fa-inbox text-4xl lg:text-6xl text-gray-300 mb-4"></i>
                <h3 class="text-lg lg:text-xl font-semibold text-gray-600 mb-2">Nenhuma instância encontrada</h3>
                <p class="text-sm lg:text-base text-gray-500">Este livro não possui instâncias cadastradas.</p>
            </div>
        `;
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        const livroInfo = document.getElementById('livroInfo');
        const instanciasContainer = document.getElementById('instanciasContainer');
        const error = document.getElementById('error');
        
        if (show) {
            loading.classList.remove('hidden');
            livroInfo.classList.add('hidden');
            instanciasContainer.classList.add('hidden');
            error.classList.add('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }

    mostrarErro(mensagem) {
        const error = document.getElementById('error');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = mensagem;
        error.classList.remove('hidden');
        
        document.getElementById('livroInfo').classList.add('hidden');
        document.getElementById('instanciasContainer').classList.add('hidden');
    }

    renderBotaoLocalizar(instancia) {
        const isEmprestado = instancia.situacao === 'emprestado';
        
        if (isEmprestado) {
            // Botão inativo para livros emprestados
            return `
                <button 
                    class="bg-gray-400 text-white px-3 py-2 rounded-lg cursor-not-allowed flex items-center justify-center text-sm font-medium w-full sm:w-auto opacity-60"
                    disabled
                    title="Não é possível localizar - livro emprestado"
                >
                    <i class="fas fa-ban mr-1 sm:mr-2"></i>
                    <span class="hidden sm:inline">Emprestado</span>
                    <span class="sm:hidden text-xs">Emprestado</span>
                </button>
            `;
        } else {
            // Botão ativo para livros disponíveis
            return `
                <a 
                    href="/instancias/${instancia.idInstancia}/detalhes/localizacao" 
                    class="bg-purple-600 text-white px-3 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center text-sm font-medium w-full sm:w-auto"
                    title="Localizar esta instância"
                >
                    <i class="fas fa-search-location mr-1 sm:mr-2"></i>
                    <span class="hidden sm:inline">Localizar</span>
                    <span class="sm:hidden text-xs">Localizar</span>
                </a>
            `;
        }
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new LivroDetalhes();
});
