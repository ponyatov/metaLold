def WEB():
  from flask     import Flask,render_template
  from flask_wtf import FlaskForm
  from wtforms   import TextAreaField,SubmitField
    
  web = Flask(__name__)
    
  # SECRET_KEY required for CSRF
  web.config['SECRET_KEY'] = os.urandom(32)
    
    
  # form class
  class CLI(FlaskForm):
    pad = TextAreaField('pad',
                render_kw={'rows':5,'autofocus':'true'},
                default='# put your commands here')
    go = SubmitField('go')
    
  @web.route('/', methods=['GET', 'POST'])
  def index():
    form = CLI()
    if form.validate_on_submit():
      S // String(form.pad.data) ; INTERPRET()
    return render_template('index.html',W=W,form=form)
    