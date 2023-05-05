from collections import OrderedDict
Documents1 = ["Honorable Dismissal", "Certified True Text of Diploma", "Diploma Translation", "Certified True Copy of Diploma", 
	"Course Description", "True Copy of Grades", "Certificate of Enrollment", "Transfer to Other UP Units",
	"Certificate of Non-Issuance of ID"]

Documents2 = ["Certificate of Graduation", "Certificate of No Disciplinary Action", "Certificate of No Contract", 
	"Certificate of Units Earned", "Certificate of Medium of Instruction", "Certificate of Grade Equivalence", 
	"Certificate of Non-Issuance of Honorable Dismissal for Graduates", "Certificate of Non-Issuance of S.O. Number"]


Requirements = OrderedDict([  
	("Letter from parents stating the reason for Honorable Dismissal" , ["Honorable Dismissal"]) ,
	("Signed letter stating the reason for Honorable Dismissal" , ["Honorable Dismissal"]),
	("Latest University Clearance", ["Honorable Dismissal"]),
	("Exit counseling from the Office of Counseling and Guidance" , ["Honorable Dismissal"]),
	("Official Transcript of Records", ["Honorable Dismissal"]),
	("Proof of Payment" ,  [item for sublist in [Documents1, Documents2] for item in sublist]),
	("Affidavit of Loss" , ["Certified True Text of Diploma"]),
	("Scanned Copy of Diploma" , ["Diploma Translation", "Certified True Copy of Diploma"]),
	("Preferred Format for True Copy of Grades" , ["True Copy of Grades"]),
	("Signed Form 5" , ["Certificate of Enrollment", "Certificate of Non-Issuance of ID"]),
])

Base_Prices = {
	"Honorable Dismissal" : "220",
	"Transfer to Other UP Units" : "150",
	"Certified True Copy of Diploma" : "220",
	"Diploma Translation" : "50",
	"Certified True Text of Diploma" : "20",
	"Course Description" : "20",	
	"True Copy of Grades" : "50",
	"Certificate of Enrollment" : "50",
	"Certificate of Graduation" : "50",
	"Certificate of No Disciplinary Action" : "50",
	"Certificate of No Contract" : "50",
	"Certificate of Units Earned" : "50",
	"Certificate of Medium of Instruction" : "50",
	"Certificate of Grade Equivalence" : "50",
	"Certificate of Non-Issuance of Honorable Dismissal for Graduates" : "50",
	"Certificate of Non-Issuance of S.O. Number" : "50",
	"Certificate of Non-Issuance of ID" : "50"
}

scholarship_discounted_documents = ["Certificate of Enrollment", "Certificate of No Disciplinary Action", 
"True Copy of Grades", "Certificate of Non-Issuance of ID"]


