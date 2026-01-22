"""API v1 serializers."""
from rest_framework import serializers
from clientes.models import Usuario
from servicos.models import Servico, RecursoServico
from pacotes.models import Pacote, RecursoPacote
from portfolio.models import Case, CategoriaPortfolio
from orcamentos.models import Orcamento
from projetos.models import Projeto, Milestone
from suporte.models import Ticket, RespostaTicket
from faturas.models import Fatura, ItemFatura, Pagamento
from core.models import Contato
from notificacoes.models import Notificacao


class RecursoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoServico
        fields = ['titulo_pt', 'titulo_en', 'descricao_pt', 'descricao_en', 'icone']


class ServicoSerializer(serializers.ModelSerializer):
    recursos = RecursoServicoSerializer(many=True, read_only=True)

    class Meta:
        model = Servico
        fields = [
            'id', 'tipo', 'nome_pt', 'nome_en', 'slug',
            'descricao_curta_pt', 'descricao_curta_en',
            'descricao_pt', 'descricao_en', 'icone', 'imagem',
            'tecnologias', 'beneficios_pt', 'beneficios_en',
            'recursos'
        ]


class RecursoPacoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoPacote
        fields = ['titulo_pt', 'titulo_en', 'incluido', 'destaque']


class PacoteSerializer(serializers.ModelSerializer):
    recursos = RecursoPacoteSerializer(many=True, read_only=True)
    preco_final = serializers.DecimalField(
        source='get_preco_final',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Pacote
        fields = [
            'id', 'tipo', 'nome_pt', 'nome_en', 'subtitulo_pt', 'subtitulo_en',
            'descricao_pt', 'descricao_en', 'preco', 'preco_promocional',
            'preco_final', 'tempo_desenvolvimento', 'suporte_dias',
            'horas_treinamento', 'destaque', 'recursos'
        ]


class CaseSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome_pt', read_only=True)

    class Meta:
        model = Case
        fields = [
            'id', 'titulo_pt', 'titulo_en', 'slug', 'categoria', 'categoria_nome',
            'cliente', 'industria', 'desafio_pt', 'desafio_en',
            'solucao_pt', 'solucao_en', 'resultados_pt', 'resultados_en',
            'tecnologias', 'funcionalidades', 'tempo_desenvolvimento',
            'imagem_destaque', 'imagens', 'url_projeto', 'metricas'
        ]


class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = [
            'id', 'numero', 'nome_completo', 'email', 'telefone',
            'empresa', 'cnpj', 'cidade', 'estado', 'tipo_projeto',
            'pacote', 'descricao_projeto', 'objetivos', 'publico_alvo',
            'funcionalidades', 'integracoes', 'sistema_pagamento',
            'referencia_design', 'possui_dominio', 'possui_hospedagem',
            'orcamento_disponivel', 'prazo_desejado', 'data_inicio_preferida',
            'status', 'created_at'
        ]
        read_only_fields = ['numero', 'status', 'created_at']


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'titulo', 'descricao', 'status', 'data_previsao', 'data_conclusao']


class ProjetoSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    pacote_nome = serializers.CharField(source='pacote.nome_pt', read_only=True)

    class Meta:
        model = Projeto
        fields = [
            'id', 'nome', 'slug', 'descricao', 'tecnologias',
            'status', 'progresso', 'data_inicio', 'data_previsao',
            'data_conclusao', 'pacote', 'pacote_nome', 'valor_total',
            'milestones', 'created_at'
        ]


class RespostaTicketSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.nome_completo', read_only=True)

    class Meta:
        model = RespostaTicket
        fields = ['id', 'autor', 'autor_nome', 'conteudo', 'anexos', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    respostas = RespostaTicketSerializer(many=True, read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'numero', 'assunto', 'descricao', 'categoria',
            'prioridade', 'status', 'projeto', 'projeto_nome',
            'anexos', 'respostas', 'created_at', 'updated_at'
        ]
        read_only_fields = ['numero', 'status', 'created_at', 'updated_at']


class ItemFaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFatura
        fields = ['id', 'descricao', 'quantidade', 'valor_unitario', 'subtotal']


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id', 'metodo', 'valor', 'status', 'transacao_id', 'data_pagamento']


class FaturaSerializer(serializers.ModelSerializer):
    itens = ItemFaturaSerializer(many=True, read_only=True)
    pagamentos = PagamentoSerializer(many=True, read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)

    class Meta:
        model = Fatura
        fields = [
            'id', 'numero', 'descricao', 'subtotal', 'desconto',
            'impostos', 'valor_total', 'data_emissao', 'data_vencimento',
            'data_pagamento', 'status', 'projeto', 'projeto_nome',
            'itens', 'pagamentos', 'observacoes'
        ]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'nome_completo', 'telefone', 'cpf',
            'foto', 'idioma_preferido', 'notificacoes_email',
            'notificacoes_sms', 'created_at'
        ]
        read_only_fields = ['email', 'created_at']


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['id', 'tipo', 'categoria', 'titulo', 'mensagem', 'url', 'lida', 'created_at']
