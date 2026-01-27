from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .models import Projeto, Milestone, TimelineEvento, MensagemProjeto, ArquivoProjeto


class MilestoneInline(admin.TabularInline):
    """Inline editor for project milestones."""
    model = Milestone
    extra = 3
    fields = ['titulo', 'descricao', 'status', 'data_previsao', 'data_conclusao', 'ordem']
    ordering = ['ordem']
    classes = ['collapse']


class TimelineEventoInline(admin.TabularInline):
    """Inline view for project timeline (read-only)."""
    model = TimelineEvento
    extra = 0
    fields = ['tipo', 'titulo', 'descricao', 'usuario', 'created_at']
    readonly_fields = ['tipo', 'titulo', 'descricao', 'usuario', 'created_at']
    can_delete = False
    classes = ['collapse']
    max_num = 10

    def has_add_permission(self, request, obj=None):
        return False


class ArquivoProjetoInline(admin.TabularInline):
    """Inline for project files."""
    model = ArquivoProjeto
    extra = 1
    fields = ['nome', 'arquivo', 'tipo', 'enviado_por']
    classes = ['collapse']


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    """Full-featured admin for Projects."""
    list_display = ['nome', 'cliente_link', 'status_badge', 'progresso_bar', 'milestones_status', 'valor_display', 'data_inicio', 'data_previsao']
    list_filter = ['status', 'pacote', 'data_inicio', 'created_at']
    search_fields = ['nome', 'cliente__email', 'cliente__nome_completo', 'descricao']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['-created_at']
    filter_horizontal = ['equipe']
    inlines = [MilestoneInline, ArquivoProjetoInline, TimelineEventoInline]
    save_on_top = True
    list_per_page = 20
    date_hierarchy = 'data_inicio'
    autocomplete_fields = ['cliente', 'orcamento']

    fieldsets = (
        (_('Identificação'), {
            'fields': ('nome', 'slug', 'descricao'),
            'description': _('Nome e descrição do projeto')
        }),
        (_('Tecnologias'), {
            'fields': ('tecnologias',),
            'classes': ['collapse'],
            'description': _('Lista de tecnologias separadas por vírgula')
        }),
        (_('Referências'), {
            'fields': (('cliente', 'orcamento'), 'pacote'),
            'description': _('Cliente, orçamento e pacote relacionados')
        }),
        (_('Status do Projeto'), {
            'fields': (('status', 'progresso'),),
            'description': _('Status atual e percentual de conclusão')
        }),
        (_('Datas'), {
            'fields': (('data_inicio', 'data_previsao', 'data_conclusao'),),
            'description': _('Cronograma do projeto')
        }),
        (_('Equipe'), {
            'fields': ('responsavel', 'equipe'),
            'classes': ['collapse'],
            'description': _('Responsável e membros da equipe')
        }),
        (_('Financeiro'), {
            'fields': ('valor_total', 'observacoes'),
            'classes': ['collapse']
        }),
        (_('Metadados'), {
            'fields': (('created_at', 'updated_at'),),
            'classes': ['collapse']
        }),
    )

    def cliente_link(self, obj):
        """Link to client in admin."""
        if obj.cliente:
            url = reverse('admin:clientes_usuario_change', args=[obj.cliente.pk])
            return format_html('<a href="{}">{}</a>', url, obj.cliente.nome_completo or obj.cliente.email)
        return '-'
    cliente_link.short_description = _('Cliente')

    def status_badge(self, obj):
        """Show status with colored badge."""
        colors = {
            'orcamento': 'secondary',
            'aprovado': 'info',
            'em_desenvolvimento': 'primary',
            'em_testes': 'warning',
            'revisao': 'warning',
            'concluido': 'success',
            'em_manutencao': 'info',
            'pausado': 'dark',
            'cancelado': 'danger',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'

    def progresso_bar(self, obj):
        """Show progress bar."""
        color = '#28a745' if obj.progresso >= 75 else '#ffc107' if obj.progresso >= 50 else '#17a2b8'
        return format_html(
            '<div style="width:120px;background:#eee;border-radius:10px;overflow:hidden;">'
            '<div style="width:{}%;background:{};height:18px;text-align:center;color:white;font-size:11px;line-height:18px;font-weight:bold;">'
            '{}%</div></div>',
            obj.progresso, color, obj.progresso
        )
    progresso_bar.short_description = _('Progresso')

    def milestones_status(self, obj):
        """Show milestone completion status."""
        total = obj.milestones.count()
        concluidos = obj.milestones.filter(status='concluido').count()
        if total > 0:
            return format_html(
                '<span class="badge bg-success">{}</span>/<span class="badge bg-secondary">{}</span>',
                concluidos, total
            )
        return format_html('<span style="color:#999;">-</span>')
    milestones_status.short_description = _('Marcos')

    def valor_display(self, obj):
        """Show formatted value."""
        return format_html('<strong>R$ {:,.2f}</strong>', obj.valor_total)
    valor_display.short_description = _('Valor')
    valor_display.admin_order_field = 'valor_total'

    actions = ['marcar_em_desenvolvimento', 'marcar_concluido', 'marcar_pausado', 'atualizar_progresso']

    @admin.action(description=_('Marcar como Em Desenvolvimento'))
    def marcar_em_desenvolvimento(self, request, queryset):
        queryset.update(status='em_desenvolvimento')
        self.message_user(request, _('Projetos atualizados!'))

    @admin.action(description=_('Marcar como Concluído'))
    def marcar_concluido(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='concluido', progresso=100, data_conclusao=timezone.now())
        self.message_user(request, _('Projetos marcados como concluídos!'))

    @admin.action(description=_('Marcar como Pausado'))
    def marcar_pausado(self, request, queryset):
        queryset.update(status='pausado')
        self.message_user(request, _('Projetos pausados!'))

    @admin.action(description=_('Recalcular progresso baseado nos marcos'))
    def atualizar_progresso(self, request, queryset):
        for projeto in queryset:
            total = projeto.milestones.count()
            if total > 0:
                concluidos = projeto.milestones.filter(status='concluido').count()
                projeto.progresso = int((concluidos / total) * 100)
                projeto.save()
        self.message_user(request, _('Progresso recalculado!'))


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    """Admin for project milestones."""
    list_display = ['projeto', 'titulo', 'status', 'status_badge', 'data_previsao', 'data_conclusao', 'atrasado', 'ordem']
    list_filter = ['status', 'data_previsao', 'projeto']
    list_editable = ['status', 'ordem']
    search_fields = ['titulo', 'descricao', 'projeto__nome']
    ordering = ['projeto', 'ordem']
    date_hierarchy = 'data_previsao'

    def status_badge(self, obj):
        colors = {'pendente': 'secondary', 'em_andamento': 'primary', 'concluido': 'success', 'atrasado': 'danger'}
        color = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_status_display())
    status_badge.short_description = _('Status')

    def atrasado(self, obj):
        from django.utils import timezone
        if obj.status != 'concluido' and obj.data_previsao and obj.data_previsao < timezone.now().date():
            return format_html('<span style="color:#dc3545;font-weight:bold;">⚠ Atrasado</span>')
        return format_html('<span style="color:#28a745;">✓</span>')
    atrasado.short_description = _('Prazo')

    actions = ['marcar_concluido', 'marcar_em_andamento']

    @admin.action(description=_('Marcar como Concluído'))
    def marcar_concluido(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='concluido', data_conclusao=timezone.now().date())

    @admin.action(description=_('Marcar como Em Andamento'))
    def marcar_em_andamento(self, request, queryset):
        queryset.update(status='em_andamento')


@admin.register(TimelineEvento)
class TimelineEventoAdmin(admin.ModelAdmin):
    """Admin for project timeline events."""
    list_display = ['projeto', 'tipo_badge', 'titulo', 'usuario', 'created_at']
    list_filter = ['tipo', 'created_at']
    search_fields = ['titulo', 'descricao', 'projeto__nome']
    readonly_fields = ['projeto', 'tipo', 'titulo', 'descricao', 'usuario', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def tipo_badge(self, obj):
        colors = {
            'criacao': 'primary', 'status': 'info', 'milestone': 'success',
            'mensagem': 'warning', 'arquivo': 'secondary', 'pagamento': 'success'
        }
        color = colors.get(obj.tipo, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_tipo_display())
    tipo_badge.short_description = _('Tipo')


@admin.register(MensagemProjeto)
class MensagemProjetoAdmin(admin.ModelAdmin):
    """Admin for project messages."""
    list_display = ['projeto', 'autor', 'conteudo_preview', 'lido', 'lido_icon', 'created_at']
    list_filter = ['lido', 'created_at', 'projeto']
    list_editable = ['lido']
    search_fields = ['conteudo', 'projeto__nome', 'autor__email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def conteudo_preview(self, obj):
        preview = obj.conteudo[:80] + '...' if len(obj.conteudo) > 80 else obj.conteudo
        return format_html('<span title="{}">{}</span>', obj.conteudo, preview)
    conteudo_preview.short_description = _('Mensagem')

    def lido_icon(self, obj):
        if obj.lido:
            return format_html('<span style="color:#28a745;">✓ Lido</span>')
        return format_html('<span style="color:#dc3545;font-weight:bold;">● Novo</span>')
    lido_icon.short_description = _('Status')

    actions = ['marcar_como_lido', 'marcar_como_nao_lido']

    @admin.action(description=_('Marcar como lido'))
    def marcar_como_lido(self, request, queryset):
        queryset.update(lido=True)

    @admin.action(description=_('Marcar como não lido'))
    def marcar_como_nao_lido(self, request, queryset):
        queryset.update(lido=False)


@admin.register(ArquivoProjeto)
class ArquivoProjetoAdmin(admin.ModelAdmin):
    """Admin for project files."""
    list_display = ['nome', 'projeto', 'tipo_badge', 'tamanho_display', 'enviado_por', 'created_at']
    list_filter = ['tipo', 'created_at', 'projeto']
    search_fields = ['nome', 'descricao', 'projeto__nome']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def tipo_badge(self, obj):
        colors = {
            'documento': 'primary', 'imagem': 'success', 'video': 'danger',
            'codigo': 'warning', 'outro': 'secondary'
        }
        color = colors.get(obj.tipo, 'secondary')
        return format_html('<span class="badge bg-{}">{}</span>', color, obj.get_tipo_display())
    tipo_badge.short_description = _('Tipo')

    def tamanho_display(self, obj):
        if obj.arquivo:
            size = obj.arquivo.size
            if size < 1024:
                return f'{size} B'
            elif size < 1024 * 1024:
                return f'{size/1024:.1f} KB'
            else:
                return f'{size/(1024*1024):.1f} MB'
        return '-'
    tamanho_display.short_description = _('Tamanho')
