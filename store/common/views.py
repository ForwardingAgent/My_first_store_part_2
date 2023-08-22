class TitleMixin():  # 7.8 
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(*kwargs)
        context['title'] = self.title
        return context
