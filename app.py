from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate_credit_score(income, applicant_emi,
                           coapplicant_emi, bureau_history):

    # FOIR includes applicant and co-applicant EMI
    total_emi = applicant_emi + coapplicant_emi
    foir = (total_emi / income) * 100

    score = 0
    reasons = []

    # Income scoring
    if income >= 50000:
        score += 40
        reasons.append("Good income")

    elif income >= 25000:
        score += 25
        reasons.append("Moderate income")

    else:
        score += 10
        reasons.append("Low income")

    # Financial obligations
    if foir <= 30:
        score += 30
        reasons.append("Low financial obligations")

    elif foir <= 50:
        score += 20
        reasons.append("Moderate financial obligations")

    else:
        score += 5
        reasons.append("High financial obligations")

    # Bureau history
    if bureau_history == "good":
        score += 30
        reasons.append("Good bureau history")

    elif bureau_history == "average":
        score += 20
        reasons.append("Average bureau history")

    elif bureau_history == "poor":
        score += 5
        reasons.append("Poor bureau history")

    else:
        # Missing history should not get zero
        score += 15
        reasons.append(
            "Bureau history unavailable - manual review"
        )

    # Final decision
    if score >= 75 and foir <= 50:
        decision = "APPROVE"

    elif score >= 50:
        decision = "REFER"

    else:
        decision = "DECLINE"

    return score, foir, decision, reasons


@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.json

    income = float(data["income"])
    applicant_emi = float(data["applicantEmi"])
    coapplicant_emi = float(data["coApplicantEmi"])
    bureau_history = data["bureau"]

    score, foir, decision, reasons = calculate_credit_score(
        income,
        applicant_emi,
        coapplicant_emi,
        bureau_history
    )

    return jsonify({
        "score": score,
        "foir": round(foir, 2),
        "decision": decision,
        "reasons": reasons
    })


@app.route("/")
def home():
    return "Loan Credit Scoring Backend is Running"


if __name__ == "__main__":
    app.run(debug=True)
