"""
Brython MDCComponent: MDCButton
===============================
"""
from .core import MDCTemplate


########################################################################
class MDCButton(MDCTemplate):
    """"""

    NAME = 'button', 'MDCButton'

    CSS_classes = {
        'raised': 'mdc-button--raised',
        'unelevated': 'mdc-button--unelevated',
        'outlined': 'mdc-button--outlined',
        'dense': 'mdc-button--dense',
        # 'icon': 'mdc-button__icon',
    }

    MDC_optionals = {

        'reversed': 'style = "margin-left: 8px; margin-right: -4px;"',
        # 'ripple': 'data-mdc-auto-init="MDCRipple"',
        'icon': '<i class="material-icons mdc-button__icon" {reversed} aria-hidden="true">{icon}</i>',
        'icon_': '<i class="material-icons" tabindex="0" role="button" title="">{icon_}</i>',
        'disabled': 'disabled',



    }

    # ----------------------------------------------------------------------

    def __new__(self, text=None, href=None, icon=False, **kwargs):
        """"""
        icon_ = icon
        self.element = self.render(locals(), kwargs)
        return self.element

    # ----------------------------------------------------------------------

    @classmethod
    def __html__(cls, **context):
        """"""

        if context.get('href'):
            if context.get('text'):
                if not context.get('reversed'):
                    code = """
                        <a href="{href}" class="mdc-button {CSS_classes}" {disabled}>
                        {icon}
                        {text}
                        </a>
                    """
                else:
                    code = """
                        <a href="{href}" class="mdc-button {CSS_classes}" {disabled}>
                        {text}
                        {icon}
                        </a>
                    """
            else:
                code = """
                {icon}
                """

        else:
            if context.get('text'):
                if not context.get('reversed'):
                    code = """
                        <button class="mdc-button {CSS_classes}" {disabled}>
                        {icon}
                        {text}
                        </button>
                    """
                else:
                    code = """
                        <button class="mdc-button {CSS_classes}" {disabled}>
                        {text}
                        {icon}
                        </button>
                    """
            else:
                code = """
                    {icon_}
                    """

        return cls.render_html(code, context)


########################################################################
class MDCFab(MDCButton):
    """"""

    CSS_classes = {
        'mini': 'mdc-fab--mini',
        'exited': 'mdc-fab--exited',
    }

    # ----------------------------------------------------------------------

    def __new__(self, icon, **kwargs):
        """"""
        self.element = self.render(locals(), kwargs)
        return self.element

    # ----------------------------------------------------------------------

    @classmethod
    def __html__(cls, **context):
        """"""
        code = """
            <button class="mdc-fab material-icons {CSS_classes}" {disabled}>
              <span class="mdc-fab__icon">
                {icon}
              </span>
            </button>
        """

        return cls.render_html(code, context)


########################################################################
class MDCIconToggle(MDCButton):
    """"""

    NAME = '', ''
    # NAME = 'iconToggle', 'MDCIconToggle'

    # ----------------------------------------------------------------------
    def __new__(self, icon_on, icon_off=None, event_on=None, event_off=None, **kwargs):
        """"""
        self.element = self.render(locals(), kwargs)
        self.element.bind('click', self.toogle_icon(self.element, bool(icon_off)))

        self.element.event_on = event_on
        self.element.event_off = event_off

        return self.element

    # ----------------------------------------------------------------------
    @classmethod
    def toogle_icon(self, element, secondary_icon):
        """"""
        def inset(event):
            # print("ok", element)

            # print(element.attrs['state'])
            if element.attrs['state'] == 'on':
                current = 'off'
                old = 'on'
                # print('off', element.event_off)
                if not element.event_off is None:
                    element.event_off()
            elif element.attrs['state'] == 'off':
                current = 'on'
                old = 'off'
                # print('on')
                if not element.event_on is None:
                    element.event_on()

            element.attrs['state'] = current
            if secondary_icon:
                element.select(f'.radiant-icon-{current}')[0].style = {'display': 'block', }
                element.select(f'.radiant-icon-{old}')[0].style = {'display': None, }
            else:
                if current == 'on':
                    element.select(f'.radiant-icon-on')[0].style = {'display': 'block', 'opacity': 1, }
                else:
                    element.select(f'.radiant-icon-on')[0].style = {'display': 'block', 'opacity': 0.2, }

        return inset

    # ----------------------------------------------------------------------
    @classmethod
    def __html__(cls, **context):
        """"""
        if context['icon_on'].startswith('fa'):
            code = """
                <i class="mdc-icon-toggle" state="on" role="button" aria-pressed="false" {disabled} aria-label="">
                    <i class="radiant-icon-on {icon_on}"></i>
                    <i class="radiant-icon-off {icon_off}" style="display: none"></i>
                </i>
            """

        else:
            code = """
                <i class="mdc-icon-toggle" state="on" role="button" aria-pressed="false" {disabled} aria-label="">
                    <i class="radiant-icon-on mdi mdi-{icon_on}"></i>
                    <i class="radiant-icon-off mdi mdi-{icon_off}" style="display: none"></i>
                </i>
            """

        return cls.render_html(code, context)
