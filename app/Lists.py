from collections import OrderedDict
Documents1 = ["Honorable Dismissal", "Certified True Text of Diploma ", "Diploma Translation", "Certified True Copy of Diploma", 
	"Course Description", "True Copy of Grades", "Certificate of Enrollment", "Transfer to Other UP Units"]

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
	("Signed Form 5" , ["Certificate of Enrollment"]),
])




