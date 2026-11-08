"""Review-only candidate for PolicyEngine-US: New Hampshire FANF grant amount.

Not an installed PolicyEngine module. Scope is the unadjusted FANF monthly
benefit. Citation: He-W 670.03(b)(1)-(5), official New Hampshire rules.
Requires separate rule-effective-date and PolicyEngine parameterization review
before upstream deployment or benefit-screening use.
"""
from policyengine_us.model_api import *


class nh_fanf(Variable):
    value_type = float
    entity = SPMUnit
    label = "New Hampshire Financial Assistance to Needy Families"
    unit = USD
    definition_period = MONTH
    reference = (
        "https://gc.nh.gov/rules/state_agencies/he-w600.html",
        "https://gc.nh.gov/rsa/html/xii/167/167-77-g.htm",
    )
    defined_for = "nh_fanf_eligible"

    def formula(spm_unit, period, parameters):
        payment_standard = spm_unit("nh_fanf_payment_standard", period)
        countable_income = spm_unit("nh_fanf_countable_income", period)
        unadjusted = max_(payment_standard - countable_income, 0)
        whole_dollar = np.floor(unadjusted)  # He-W 670.03(b)(3)
        # He-W 670.03(b)(4)-(5): no monthly grant under $10.
        # TODO(upstream): verify historical effective date and use a dated
        # PolicyEngine parameter instead of a literal across all periods.
        return where(whole_dollar >= 10, whole_dollar, 0)
