using System;
using System.Collections.Generic;
using System.Text;

namespace ReportCommon.ProcurementPlanWB
{
   public class SelectionConsultant
    {
        public string PriorReviewThreshold { get; set; }
        public string Category { get; set; }
        public string ProcurementMethod { get; set; }
        public string Shortlistcomprisingentirelyofnationalconsultants { get; set; }
        public string ConsultancyAssignments { get; set; }
        public string ReferenceNumber { get; set; }
        public string Descriptioncontract { get; set; }
        public long EstimatedCost { get; set; }
        public string Procurementmethod { get; set; }
        public string ReviewbyBank { get; set; }
        public DateTime ExpectedBidsOpeningTime { get; set; }
        public string Marketapproach { get; set; }
        public string Donors { get; set; }
    }
}
