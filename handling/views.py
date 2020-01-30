from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.



def duplicateCandidate(request,candidate_mail,candidate_name,candidate_jt,candidate_company,candidate_location):
    return render(request,'handling/duplicateCandidate.html',{'candidate_mail':candidate_mail,
                                                          'candidate_name':candidate_name,'candidate_jt':candidate_jt,
                                                          'candidate_company':candidate_company,
                                                          'candidate_location':candidate_location})
   
def addNewCv(request,candidate_id):
    url='/admin/handling/candidate/'+candidate_id+'/change/'
    return redirect('/admin/handling/candidate/2/change/')
  

def getKibana(request):
    return render(request,'http://127.0.0.1:5601',{})

def changelist(request):
    return redirect('/admin/handling/document/add/')
    

    
    
    
    
    
    
    
    
