using System;
using System.Collections.Generic;
using System.Text;

namespace ReportCommon.ProcurementPlan
{
   public class PartOfProcurementPlan
    {
        public string ProcurementDesignAndProcess  { get; set; }
        public ContractType  contracttype { get; set; }
        public string ProcurementAndContractRisk { get; set; }
        public string ProcurementMilestones { get; set; }
        public string ProcurementActivities { get; set; }
        public string PerformanceMetrics { get; set; }
        public string RolesResponsabilitiesAndSignOffAutorities { get; set; }
        public string AssumptionsAndContraints { get; set; }
    }
}
