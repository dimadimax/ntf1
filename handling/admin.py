from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
# Register your models here.
from .models import Candidate
from .models import Position
from .models import Document
from . import elasticSearch
from django.http.response import HttpResponseRedirect
import re
from . import getValues
from . import parse
import time
from django.contrib.admin.models import LogEntry
LogEntry.objects.all().delete()



# Need to register my app so it shows up in the admin

class CandidateAdmin(admin.ModelAdmin):
        list_per_page=20
        change_list_template= "admin/candidate/change_list.html"
        list_display=['name','job_title','company','location','ral','age','education','position','mobile','email','status',
                      'author','note','cv','tag']
        list_editable=['status','position','cv']
        list_filter=['importedFrom','position__position_title','job_title','location','company','tag']
        search_fields =['name','job_title','location','company','position__position_title','tag']
        
        def get_changeform_initial_data(self,request):
            
            return {'name':toDel}
        
        def has_add_permission(self, request, obj=None):
            return False
            
        def add_view(self,request, form_url='', extra_context=None):
            print('---> Calling CandidateAdmin.add_view')
            
         
            return super(CandidateAdmin,self).add_view(request, form_url='', extra_context=None)
        
        def save_model(self, request, obj, form, change):    
            
            print('---> Calling CandidateAdmin.save_model')
            if not change: 
                
                obj.author = request.user
                
            obj.indexing()
            obj.save()
        
        def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
            extra_context = extra_context or {}
            extra_context['show_add'] = False
            
            return super(CandidateAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
            
     
        
        def delete_view(self,request, object_id, extra_context=None):
            
            print('---> Calling CandidateAdmin.delete_view')
            getPath=request.get_full_path()
            candidateID=re.search(r'\/\d.\/',getPath).group()
            candidateID=re.search(r'\d.',candidateID).group()
            try:
                self.relatedDocumentID=Candidate.objects.filter(id=candidateID)[0].cv.id
            except:
                self.relatedDocumentID=None
            self.id=int(candidateID)
            return super(CandidateAdmin, self).delete_view(request, object_id,extra_context=extra_context)
        
        
        def response_delete(self,request,obj,post_url_continue=None):
            
            print('---> Calling CandidateAdmin.response_delete')
            try:
                elasticSearch.delete(self.id)
            except:
                print('||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
                print('Error removing document '+str(obj)+' to Elasticsearch!!!\n')
                print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
            if self.relatedDocumentID:
                return redirect('/admin/handling/document/'+str(self.relatedDocumentID)+'/delete/')
        
        def delete_queryset(self,reuqest,queryset):
            
            print('---> Calling CandidateAdmin.delete_queryset')
            for obj in queryset:
                try:
                    print('id is::::::::::'+str(obj.id))
                    elasticSearch.delete(obj.id)
                except:
                    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
                    print('Error removing document '+str(obj)+' to Elasticsearch!!!\n')
                    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
                    
                try:
                    relatedDocumentID=obj.cv.id
                    Document.objects.get(id=relatedDocumentID).delete()
                except:
                    print('No document for this candidate!!!')
            return super(CandidateAdmin,self).delete_queryset(reuqest,queryset)
            
                
                
                
admin.site.register(Candidate,CandidateAdmin)

class PositionAdmin(admin.ModelAdmin):
    list_display=['position_title','location','hiring_date','budget','year_of_experience','hiring_manager','status']
    list_editable=['status']
    list_filter=['status']
    search_fields =['position_title','hiring_manager','status']
admin.site.register(Position,PositionAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display=['description','uploaded_at','author']
    #exclude=['author']

    # BIG PROBLEM: IF CANDIDATE EXSIST IT DOES'N WORK
    

    
    def add_view(self,request, form_url='', extra_context=None):
        
         print('---> Calling DocumentAdmin.add_view')
         self.fromCandidate=False
         if re.search(r'popup=',request.get_full_path()):
             print("from candidate!!!!")
             self.fromCandidate=True
         
         return super(DocumentAdmin,self).add_view(request, form_url='', extra_context=None)


    def save_model(self, request, obj, form, change):   
          
        print('---> Calling DocumentAdmin.save_model')
        if self.fromCandidate==True:
            print("from candidate ------")
            return None 
        if parse.getFormat(obj.document)=='pdf':
            print('---------------------test_html>>> pdf')
            obj.save()
            #raw_text=parse.parsePdf(obj.document)
            raw_text=parse.parsePdf(obj.document)
            obj.delete()
        mail=getValues.getMail(raw_text)
        self.mail=mail
        self.duplicateCandidate=False
        if Candidate.objects.filter(email=mail):
            print("::::::::::::::::::::::::::::::::")
            print("candidate exists")
            self.duplicateCandidate=True
            
        else:
            #define values for Candidate instance to create
            name=getValues.getName(raw_text)
            jt=getValues.getJt(raw_text)
            location=getValues.getLocation(raw_text)
            company=getValues.getCompany(raw_text)
            tags=getValues.getTags(raw_text)
            mobile=getValues.getMobile(raw_text)
            education=getValues.getEducation(raw_text)
            age=getValues.getAge(raw_text)
            obj.author = request.user
            user=obj.author
            generic=Position.objects.get(position_title='Generic Position')
            
            if obj.description=='':
               obj.description=mail
            else:
                name=obj.description
            
            obj.l=raw_text
            obj.save()
            
            newCandidate=Candidate(author=user,date=time.strftime("%Y-%m-%d"),name=name,job_title =jt,
                      company=company,location =location,age=int(age),ral=0,education=education,
                      position=generic,url='none',mobile=mobile,email=mail,cv=obj,tag=tags,rawText=obj.l,experiences='none')
            
            newCandidate.save()
            newCandidate.indexing()
        print(self.duplicateCandidate)
            
        
         
        
    def response_add(self,request,obj,post_url_continue="../%s/",force=False):
        
        
        print("---> Calling DocummentAdmin.response_add")
        if self.fromCandidate==True:
            print("self.fromCandidate==True from response_add from DocumentAdmin")
            if parse.getFormat(obj.document)=='pdf':
                print('---------------------test_html>>> pdf')
                obj.save()
               # raw_text=parse.parsePdf(obj.document)
                raw_text=parse.parsePdf(obj.document)
                obj.description=getValues.getMail(raw_text)
                obj.save()
         
            return super(DocumentAdmin,self).response_add(request,obj,post_url_continue)

        if self.duplicateCandidate==True:
            candidateInstance=Candidate.objects.get(email=self.mail)
            
            candidateToDuplicate=Candidate.objects.get(email=self.mail)
            candidate_name=candidateToDuplicate.name
            candidate_location=candidateToDuplicate.location
            candidate_jt=candidateToDuplicate.job_title
            candidate_company=candidateToDuplicate.company
            print("return HttpResponse!!!!")
            return HttpResponseRedirect(reverse("handling:duplicateCandidate",kwargs={'candidate_mail': self.mail,
                'candidate_name':candidate_name,'candidate_jt':candidate_jt,'candidate_company':candidate_company,
                'candidate_location':candidate_location}))
        
        else:
           print("check outside candidate from CV")
           print("here check if candidate exists as scraped from linkedin") 
           return redirect('/admin/handling/candidate/')
    
                
                
                #'candidate_location':candidate_location,
                #'candidate_jt':caandidate_jt,'candidate_company':candidate_company}))
                
            
        obj.user=request.user
        try:
            documentId=str(max([i.id for i in Document.objects.all()]))
            candidateId=str(Candidate.objects.get(cv_id=documentId).id)
        except:
            None
       
        #candidateId=str(Candidate.objects.all()[len(Candidate.objects.all())-1].id)
        if '_continue' in request.POST:
            
            documentId=str(max([i.id for i in Document.objects.all()]))
            return super(DocumentAdmin,self).response_add(request,obj,post_url_continue='/admin/handling/document/'+documentId+'/change/')
        
        if '_addanother' in request.POST:
            return super(DocumentAdmin,self).response_add(request,obj,post_url_continue='/admin/ntf/document/add/')
        
        
        else:
                       
            return redirect('/admin/handling/candidate/'+candidateId+'/change')
    
    def delete_view(self,request, object_id, extra_context=None):
        
            print('---> Calling DocumentAdmin.delete_view')
            
            self.candidateIDToDel=Candidate.objects.filter(cv=Document.objects.get(id=object_id))[0].id
            return super(DocumentAdmin, self).delete_view(request, object_id,extra_context=extra_context)
     

    def delete_queryset(self,reuqest,queryset):
        
            print('---> Calling DocumentAdmin.delete_queryset')
            for obj in queryset:
                candidateIDToDel=Candidate.objects.filter(cv=obj)[0].id
               # delete(candidateIDToDel)
                try:
                  #  candidateIDToDel=Candidate.objects.filter(cv=obj).id
                     elasticSearch.delete(candidateIDToDel)
                except:
                    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
                    print('Error removing document '+str(obj)+' to Elasticsearch!!!\n')
                    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
                    
            return super(DocumentAdmin,self).delete_queryset(reuqest,queryset)
        
    def response_delete(self,request,obj,post_url_continue=None):
        
            print('---> Calling DocumentAdmin.response_delete')
            elasticSearch.delete(self.candidateIDToDel)
            return redirect('/admin/handling/candidate')
    
   

admin.site.register(Document,DocumentAdmin)