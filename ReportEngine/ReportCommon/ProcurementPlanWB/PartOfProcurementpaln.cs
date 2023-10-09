using System;
using System.Collections.Generic;
using System.Text;

namespace ReportCommon.ProcurementPlanWB
{
    public class PartOfProcurementplan
    {
        public ProjectInformations projectinformation { get; set; }
        public string BanksapprovaldateofProcurementplan { get; set; }
        public string DateofGeneralProcurementNotice { get; set; }
        public DateTime Periodcoveredbythisprocurementplan { get; set; }
        public WorksandGoodsandNonConsultantServices worksandGoodsandNonConsultantServices { get; set; }
        public SelectionofConsultant selectionofConsultants { get; set; }
    }
}
