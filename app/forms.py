# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
 
from wtforms import EmailField, PasswordField, TextAreaField, FileField, StringField, IntegerField,DecimalField
from wtforms.validators import   Email, DataRequired, InputRequired

class UploadForm(FlaskForm):
    """UploadForm"""
    photo        = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!') ])
    description  = TextAreaField('Description' )


class LoginForm(FlaskForm):
    """LoginForm"""
    email               = EmailField("E-mail",validators=[DataRequired(),Email()])
    password            = PasswordField("Password", validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    """RegistrationForm"""
    firstname           = StringField("Firstname",validators=[DataRequired()])
    lastname            = StringField("Lastname",validators=[DataRequired()])
    email               = EmailField("E-mail",validators=[DataRequired(),Email()])
    password            = PasswordField("Password", validators=[InputRequired()])
    passwordConfirm     = PasswordField("Confirm", validators=[InputRequired()])
    code                = StringField("Code",validators=[DataRequired()])


class ProductForm(FlaskForm):
    """ProductForm"""
    
    Name                = StringField("Name",validators=[DataRequired()])
    Ref                 = StringField("Ref Number",validators=[DataRequired()])
    Ref1                = StringField("Ref1 Number",validators=[ ])
    Description         = StringField("Description",validators=[DataRequired()])
    Type                = StringField("Type",validators=[])
    Details             = StringField("Details",validators=[])  
    images              = FileField('Photo', validators=[ FileAllowed(['jpg', 'png'], 'Images only!') ]) 
    UnitQuantity        = IntegerField("UnitQuantity",validators=[DataRequired()])
    Cost                = DecimalField("Cost",validators=[DataRequired()])
    Threshold           = IntegerField("Threshold",validators=[DataRequired()])




class SiteForm(FlaskForm):
    """SiteForm"""    
    Name                = StringField("Name",validators=[DataRequired()])
    Address             = StringField("Address",validators=[DataRequired()])
    Country             = StringField("Country ",validators=[DataRequired()])  
    

class LocationForm(FlaskForm):
    """LocationForm"""
    Site         = StringField("Site",validators=[DataRequired()])
    Name         = StringField("Name",validators=[DataRequired()])


class ShelveForm(FlaskForm):
    """ShelveForm"""
    Site         = StringField("Site",validators=[DataRequired()])
    Location     = StringField("Location",validators=[DataRequired()])
    Shelf        = StringField("Shelf",validators=[DataRequired()])   


class StowForm(FlaskForm):
    """StowForm"""
    User         = StringField("User",validators=[DataRequired()])
    Operation    = StringField("Operation",validators=[DataRequired()])
    Site         = StringField("Site",validators=[DataRequired()])
    Location     = StringField("Location",validators=[DataRequired()])
    Shelf        = StringField("Shelf",validators=[DataRequired()]) 
    Product      = StringField("Product",validators=[DataRequired()]) 
    Quantity     = IntegerField("Quantity",validators=[DataRequired()])


class RelocationForm(FlaskForm):
    """RelocationForm"""
    User         = StringField("User",validators=[DataRequired()])
    Site         = StringField("Site",validators=[DataRequired()])
    Location     = StringField("Location",validators=[DataRequired()])
    Location1    = StringField("Location1",validators=[DataRequired()])
    Shelf        = StringField("Shelf",validators=[DataRequired()]) 
    Shelf1       = StringField("Shelf1",validators=[DataRequired()]) 
    Product      = StringField("Product",validators=[DataRequired()]) 



class OrderUpdateForm(FlaskForm):
    """OrderUpdateForm"""
  
    OrderID             = StringField("OrderID",validators=[DataRequired()])
    Tracking            = StringField("Tracking",validators=[])
    Method              = StringField("Method",validators=[])
    Invoice             = FileField('Invoice', validators=[ FileAllowed(['jpg', 'png','pdf'] ) ]) 
 
