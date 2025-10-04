from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import datetime
import logging

logger = logging.getLogger(__name__)

def asthma_page(request):
    """
    Render the asthma assessment page
    """
    return render(request, 'asthma/asthma.html')

@csrf_exempt
@require_http_methods(["POST"])
def update_record(request):
    """
    Handle asthma assessment form submission and update patient record
    """
    try:
        # Extract form data
        patient_id = request.POST.get('patientId', '').strip()
        assessment_date = request.POST.get('assessmentDate', '')
        notes = request.POST.get('notes', '').strip()
        
        # Extract symptom data
        peak_flow = request.POST.get('peakFlow', '')
        breathing = request.POST.get('breathing', '')
        cough = request.POST.get('cough', '')
        wheezing = request.POST.get('wheezing', '')
        
        # Extract environment data
        environment = request.POST.get('environment', '')
        triggers = request.POST.get('triggers', '')
        
        # Extract medication data
        inhaler_usage = request.POST.get('inhalerUsage', '')
        effectiveness = request.POST.get('effectiveness', '')
        
        # Validate required fields
        if not patient_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Patient ID is required'
            }, status=400)
        
        if not assessment_date:
            return JsonResponse({
                'status': 'error',
                'message': 'Assessment date is required'
            }, status=400)
        
        # Create assessment record
        assessment_data = {
            'patient_id': patient_id,
            'assessment_date': assessment_date,
            'timestamp': datetime.datetime.now().isoformat(),
            'symptoms': {
                'peak_flow': peak_flow,
                'breathing_difficulty': breathing,
                'cough_frequency': cough,
                'wheezing': wheezing
            },
            'environment': {
                'current_environment': environment,
                'trigger_exposure': triggers
            },
            'medication': {
                'inhaler_usage_today': inhaler_usage,
                'medication_effectiveness': effectiveness
            },
            'notes': notes
        }
        
        # Log the assessment for debugging
        logger.info(f"Asthma assessment received for patient {patient_id}: {assessment_data}")
        
        # Here you would typically save to database
        # For now, we'll simulate a successful save
        success = save_asthma_assessment(assessment_data)
        
        if success:
            # Determine severity level for response
            severity = determine_severity(assessment_data)
            
            response_message = f"Assessment submitted successfully for Patient {patient_id}."
            
            # Add severity-based recommendations
            if severity == 'high':
                response_message += " ⚠️ High severity symptoms detected. Please consult your doctor immediately."
            elif severity == 'medium':
                response_message += " ⚠️ Moderate symptoms detected. Monitor closely and consider contacting your healthcare provider."
            else:
                response_message += " ✅ Symptoms appear manageable. Continue with current treatment plan."
            
            return JsonResponse({
                'status': 'success',
                'message': response_message,
                'severity': severity,
                'patient_id': patient_id,
                'assessment_id': f"ASTHMA_{patient_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to save assessment. Please try again.'
            }, status=500)
            
    except Exception as e:
        logger.error(f"Error processing asthma assessment: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred while processing your assessment. Please try again.'
        }, status=500)

def save_asthma_assessment(assessment_data):
    """
    Save asthma assessment to database or external system
    This is a placeholder function - implement actual database logic here
    """
    try:
        # TODO: Implement actual database save logic
        # Example:
        # AsthmaAssessment.objects.create(**assessment_data)
        
        # For now, just log the data and return success
        logger.info(f"Saving asthma assessment: {json.dumps(assessment_data, indent=2)}")
        
        # Simulate successful save
        return True
        
    except Exception as e:
        logger.error(f"Error saving asthma assessment: {str(e)}")
        return False

def determine_severity(assessment_data):
    """
    Determine severity level based on assessment data
    """
    severity_score = 0
    
    symptoms = assessment_data.get('symptoms', {})
    medication = assessment_data.get('medication', {})
    
    # Peak flow scoring
    peak_flow = symptoms.get('peak_flow', '')
    if peak_flow == 'danger':
        severity_score += 3
    elif peak_flow == 'caution':
        severity_score += 2
    
    # Breathing difficulty scoring
    breathing = symptoms.get('breathing_difficulty', '')
    if breathing == 'severe':
        severity_score += 3
    elif breathing == 'moderate':
        severity_score += 2
    elif breathing == 'mild':
        severity_score += 1
    
    # Wheezing scoring
    wheezing = symptoms.get('wheezing', '')
    if wheezing == 'severe':
        severity_score += 3
    elif wheezing == 'moderate':
        severity_score += 2
    elif wheezing == 'mild':
        severity_score += 1
    
    # Cough frequency scoring
    cough = symptoms.get('cough_frequency', '')
    if cough == 'persistent':
        severity_score += 2
    elif cough == 'frequent':
        severity_score += 1
    
    # Inhaler usage scoring
    inhaler_usage = medication.get('inhaler_usage_today', '')
    if inhaler_usage == '5+':
        severity_score += 3
    elif inhaler_usage == '3-4':
        severity_score += 2
    elif inhaler_usage == '1-2':
        severity_score += 1
    
    # Medication effectiveness scoring
    effectiveness = medication.get('medication_effectiveness', '')
    if effectiveness == 'poor':
        severity_score += 2
    elif effectiveness == 'fair':
        severity_score += 1
    
    # Determine severity level
    if severity_score >= 8:
        return 'high'
    elif severity_score >= 4:
        return 'medium'
    else:
        return 'low'

@csrf_exempt
def get_patient_history(request):
    """
    Get patient's asthma assessment history
    """
    if request.method == 'GET':
        patient_id = request.GET.get('patient_id', '')
        
        if not patient_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Patient ID is required'
            }, status=400)
        
        try:
            # TODO: Implement actual database query
            # history = AsthmaAssessment.objects.filter(patient_id=patient_id).order_by('-assessment_date')
            
            # For now, return mock data
            mock_history = [
                {
                    'assessment_date': '2025-01-27',
                    'severity': 'low',
                    'peak_flow': 'normal',
                    'inhaler_usage': '1-2'
                },
                {
                    'assessment_date': '2025-01-26',
                    'severity': 'medium',
                    'peak_flow': 'caution',
                    'inhaler_usage': '3-4'
                }
            ]
            
            return JsonResponse({
                'status': 'success',
                'patient_id': patient_id,
                'history': mock_history
            })
            
        except Exception as e:
            logger.error(f"Error retrieving patient history: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Error retrieving patient history'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)
