from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .elasticSearch import mapping 
from django.core.validators import EmailValidator
# Create your models here.

# Blogpost to be indexed into ElasticSearch

#this class is an example for uploading files

emailvalidator = EmailValidator(message="invalid email")


class Position(models.Model):
    position_title=models.CharField(max_length=200,db_index=True)
    location=models.CharField(max_length=200,db_index=True)
    hiring_date=models.DateField(default=timezone.now)
    budget=models.PositiveIntegerField()
    year_of_experience=models.PositiveIntegerField()
    hiring_manager= models.CharField(max_length=200,default='None')
    statusChoice = (
        ('Z','To be start'),
        ('A', 'On going'),
        ('B', 'Offer'),
        ('C', 'Filled'),
        ('D','Stand-by'),
        ('E','Cancelled'),
   )
    status=models.CharField(max_length=2, choices=statusChoice,default='To be start')
    
    class Meta:
        verbose_name='position'
        verbose_name_plural='Handling Positions'
    
    def __str__(self):
        return self.position_title
    

class Document(models.Model):
    description = models.CharField(max_length=255,verbose_name='CV',blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True,verbose_name='UPLOADED AT')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Document',null=True,editable=False,verbose_name='USER')
    l=models.TextField(max_length=20000,verbose_name='Raw Text',default='None')
    class Meta:
        verbose_name='CV'
        verbose_name_plural='Upload candidates from CV'

    def __str__(self):
      
      return '%s' % (self.description)
   

class Candidate(models.Model):
    
   cv=models.ForeignKey(Document,related_name='Cv',on_delete=models.CASCADE,null=True,blank=True)
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Candidate',verbose_name='USER',editable=False)
   date = models.DateField(default=timezone.now)
   name = models.CharField(max_length=200)
   job_title = models.CharField(max_length=200)
   company = models.CharField(max_length=200)
   location = models.CharField(max_length=200)
   age = models.PositiveIntegerField()
   ral = models.PositiveIntegerField()
   education=models.CharField(max_length=50)
   position=models.ForeignKey(Position,related_name='Position',on_delete=models.CASCADE)
   mobile=models.CharField(max_length=50)
   email=models.CharField(max_length=200,validators=[emailvalidator])
   url=models.CharField(max_length=200,null=True)
   tag=models.CharField(max_length=200)
   importedFrom=models.CharField(max_length=200,verbose_name='Imported from',default='CV')
   rawText=models.CharField(max_length=200000000000,null=True)
   experiences=models.CharField(max_length=200,null=True)
   statusChoice = (
        ('Z','Prospect'),
        ('A', 'To Call'),
        ('B', 'Recall'),
        ('C', 'Not Interested'),
        ('D','Waiting feedback'),
        ('E','1° interview'),
        ('F','2° interview'),
        ('G','Lack of hard skills'),
        ('H','Lack of soft skills'),
        ('I','Retired'),
        ('L','Under Offer'),
        ('M','Refuse Offer'),
        ('N','Filled'),
   )
   status=models.CharField(max_length=2, choices=statusChoice,default='Prospect')
   d={}
   for i in statusChoice:
       d[i[0]]=i[1]
   note = models.TextField(max_length=200,default='None about this candidate')
   
   class Meta:
      ordering = ["name"]
      verbose_name_plural = " Handling Candidates"
      unique_together = ["email","name"]
   def __str__(self):
      return '%s' % (self.name)
  

#indexing to elasticsearch 
      
   def indexing(self):
     
      try:
          getText=self.cv.l
      except:
          getText=self.rawText #coming from selenium
      obj = mapping(
      meta={'id': self.id},
      author=self.author.username,
      date=self.date,
      ral=self.ral,
      name = self.name,
      job_title = self.job_title,
      company = self.company,
      location = self.location,
      education=self.education,
      raw_text=getText,
      status=str(self.d.get(self.status)),
      note = self.note,
      tags=self.tag,
      email=self.email,
      url=self.url,
      mobile=self.mobile,
      importedFrom=self.importedFrom,
      related_to=self.position.position_title,
      experiences=self.experiences)
      obj.save()
      return obj.to_dict(include_meta=True)
  



