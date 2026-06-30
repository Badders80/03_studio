import jinja2
import argparse
import os
from datetime import datetime

def calculate_payout(data):
    """
    Logic:
    1. Lease pool = 5% of total eligible NZD
    2. Investor pool = 75% of lease pool
    3. Per token NZD = Investor pool / tokens
    4. Payout AED = Per token NZD * FX rate (rounded to 2 decimal places)
    """
    lease_pool = data["total_eligible_nzd"] * 0.05
    investor_pool = lease_pool * 0.75
    per_token_nzd = investor_pool / data["tokens"]
    return round(per_token_nzd * data["fx"], 2)

def generate_report(data, template_path, output_path):
    if not os.path.exists(template_path):
        # Try absolute path if relative fails
        if not os.path.isabs(template_path):
            alt_path = os.path.join(os.getcwd(), template_path)
            if os.path.exists(alt_path):
                template_path = alt_path
            else:
                print(f"Template not found: {template_path}")
                return
        else:
            print(f"Template not found: {template_path}")
            return

    template_dir = os.path.dirname(template_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(os.path.basename(template_path))

    # Calculate payout and add to data
    data['payout_aed'] = calculate_payout(data)

    # Derived data for template
    data['lease_share_nzd'] = f"{data['total_eligible_nzd'] * 0.05:,.2f}"
    data['distribution_stakes_nzd'] = f"{data['total_eligible_nzd']:,.2f}"
    data['total_stakes_nzd'] = data.get('total_stakes_nzd', f"{data['total_eligible_nzd']:,.2f}")

    # Prudentia Specifics
    data['horse_name'] = data.get('horse_name', "Prudentia")
    data['asset_id'] = data.get('asset_id', "10")
    data['report_date'] = data.get('report_date', "30 June 2026")
    data['report_period'] = data.get('report_period', "Q1/Q2 2026")

    output = template.render(data)

    # Ensure output path is absolute or relative to cwd
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(output)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Prudentia Investor Report")
    # Support both underscore and dash versions
    parser.add_argument("--total-eligible-nzd", "--total_eligible_nzd", type=float, help="Total eligible NZD (the distribution pool)")
    parser.add_argument("--total-stakes-nzd", type=float, help="Total stakes earned by the horse (100% ownership)")
    parser.add_argument("--tokens", type=int, help="Number of tokens")
    parser.add_argument("--fx", type=float, help="FX Rate NZD to AED")
    parser.add_argument("--slug", type=str, help="Report slug for output filename")
    parser.add_argument("--template", type=str, default="03_studio/templates/investor_report_institutional_lite.html")
    parser.add_argument("--output", type=str, help="Output path (optional, overrides slug)")

    args = parser.parse_args()

    total_nzd = args.total_eligible_nzd
    if total_nzd and args.tokens and args.fx:
        output_path = args.output
        if not output_path and args.slug:
            output_path = f"02_website/public/updates/{args.slug}.html"
        elif not output_path:
            output_path = "03_studio/output/investor_report.html"

        data = {
            "total_eligible_nzd": total_nzd,
            "tokens": args.tokens,
            "fx": args.fx
        }
        if args.total_stakes_nzd:
            data["total_stakes_nzd"] = f"{args.total_stakes_nzd:,.2f}"
        generate_report(data, args.template, output_path)
    else:
        print("Missing required arguments. Use --help for usage.")
