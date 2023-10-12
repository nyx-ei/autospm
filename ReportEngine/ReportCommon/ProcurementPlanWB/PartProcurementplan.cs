using System;
using System.Collections.Generic;
using System.Text;

namespace ReportCommon.ProcurementPlanWB
{
    public class PartProcurementPlan
    {
        public ProjectInformations projectInformation { get; set; }
        public string BanksapprovaldateofProcurementplan { get; set; }
        public string DateofGeneralProcurementNotice { get; set; }
        public DateTime Periodcoveredbythisprocurementplan { get; set; }
        public WorksGoodsNonConsultantServices worksGoodsNonConsultantServices { get; set; }
        public SelectionConsultant selectionConsultants { get; set; }
    }
}
