# -*- coding: utf-8 -*-
from zope.interface import Interface
from five import grok
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.security import checkPermission

from liberiun.govtiles.models.commentcontent import CommentContent, Status


"""

    Serão definidas as views/macros dos comentários para os conteúdos
    
"""

grok.templatedir('templates')

class CommentContentMacro(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('comment-content-macro')
    """
    
        View que fica abaixo do conteúdo, mostra os campos para comentar, e os comentários válidos.
        
    """
    
    def load_view(self):
        self.p_membership = self.context.portal_membership
        form = self.request.form
        self.user_logged = self.p_membership.getAuthenticatedMember()
        
        if self.user_logged.getUserName() ==  'Anonymous User':
            self.is_anonymous = True
        else:
            self.is_anonymous = False
            self.member = self.user_logged
        
        if form.get('save'):
            self.insertNewComment(form)
            
            
    def insertNewComment(self, form):
        """
            Insere um novo comentário no banco de dados
            
            @param form: Dicionario vindo o request com os dados do formulário
            @return: Registro criado no BD
        """
        
        if self.user_logged.getUserName() == 'Anonymous User':
            name = form.get('name')
            email = form.get('email')
        else:
            name = self.user_logged.getProperty('fullname')
            email = self.user_logged.getProperty('email')
            
        username = self.user_logged.getUserName()
        
        data = {'uid': self.context.UID(),
                'name': name,
                'email': email,
                'username': username,
                'text': form.get('text', ''),}
        comment = CommentContent().newCommentContent(**data)
        
        return comment
    
    def getApprovedReplies(self):
        """
            Método retorna um dicionario com as respostas aprovadas pelo gestor
            
            @return: Retorna um query set com os registros
        """
        uid = self.context.UID()
        return CommentContent().getApprovedComments(uid)
    
    def getPendingReplies(self):
        """
            Método retorna um dicionario com as respostas pendentes pelo gestor
            
            @return: Retorna um query set com os registros
        """
        uid = self.context.UID()
        return CommentContent().getPendingComments(uid)
        
    
    def getDataReplies(self):
        """
            Método retorna um dicionario com os dados dos comentários do conteúdo do contexto
            
            @return: Retorna o dicionario com os dados - qtd_replies - Quandidade de respostas no conteúdo
                                                         qtd_pending - Quantidade de respostas pendenetes
                                                         data - Lista de comentarios aprovados
        """
        uid = self.context.UID()
        
        approved = self.getApprovedReplies()
        try:
            qtd_replies = approved.count()
        except TypeError:
            qtd_replies = 0
        
        pending = self.getPendingReplies()
        try:
            qtd_pending = pending.count()
        except TypeError:
            qtd_pending = 0
        
        return {'qtd_replies': qtd_replies,
                'qtd_pending': qtd_pending,
                'data': [self._reg_for_dict(reg) for reg in approved if reg]}
        
        
    def _reg_for_dict(self, reg):
        '''
            Converte um registro de comentário em um dicionário
        '''
        
        data_object =  {
            'name': reg.name,
            'email': reg.email,
            'user_url': self.getCommenterHomeUrl(reg.username),
            'created': self.datetimeToString(reg.date_created),
            'text': reg.text,
            'id': reg.id,
            'status': reg.status,
            'date_status': reg.date_status,
            'class_status': 'status-'+Status(reg.status).name,
        }
        return data_object
    
    def getCommenterHomeUrl(self, username=None):
        if username is None or username == 'Anonymous User':
            return False
        else:
            return "%s/author/%s" % (self.context.portal_url(), username)
        
    def datetimeToString(self, dt):
        return dt.strftime('%d/%m/%y, %H:%M')
    
    def canManageComments(self):
        return checkPermission('cmf.RequestReview', self.context)
    
class ManageCommentsView(CommentContentMacro):
    grok.context(Interface)
    grok.require('cmf.RequestReview')
    grok.name('manage-comments-view')
    """
    
        View para gerenciar os comentários do contexto
        
    """
    
    def update(self):
        form = self.request.form
        
        if form.get('replies'):
            self.changeStatusReplies(form)
            
    def changeStatusReplies(self, form):
        """
            Método que altera o status de uma lista de comentários
            
            @param form: Request form
        """
        
        ids = form.get('replies')
        
        if isinstance(ids, str):
            ids = [ids]
        
        if form.get('approve'):
            status = Status['aprovado']
        elif form.get('reprove'):
            status = Status['reprovado']
        else:
            return
        ids = [int(id) for id in ids if id]

        CommentContent().changeStatus(ids, status)
        
    
    def getHistoryReplies(self):
        """
            Método retorna um dicionario com as respostas aprovadas pelo gestor
            
            @return: Retorna um query set com os registros
        """
        uid = self.context.UID()
        
        return CommentContent().getHistoryComments(uid)
    
    
    
    def getDataToView(self):
        """
            Método retorna um dicionario com os dados dos comentários para a view de gerenciamento
            
            @return: Retorna o dicionario com os dados - history_replies - Lista do historico de respotas
                                                         pending_replies - Lista de comentarios pendentes
        """

        uid = self.context.UID()
        
        history = self.getHistoryReplies()
        pending = self.getPendingReplies()
        
        return {'history_replies':  [self._reg_for_dict(reg) for reg in history if reg],
                'pending_replies': [self._reg_for_dict(reg) for reg in pending if reg],}
    
    
    
    def getLabelStatus(self, reply):
        """
            Retorna o status e a hora da mudança de status
            
            @param reply: Dict de uma reposta
        """
        
        if reply:
            status = Status(reply['status'])
            date_status = self.datetimeToString(reply['date_status'])
            str_status = status.name.capitalize()
            return '%s %s' % (str_status, date_status)
            
            
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
