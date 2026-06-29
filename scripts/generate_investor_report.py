import jinja2
import argparse
import os

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
        print(f"Template not found: {template_path}")
        return

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Calculate payout and add to data
    data['payout_aed'] = calculate_payout(data)

    output = template.render(data)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(output)
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Prudentia Investor Report")
    parser.add_argument("--total_eligible_nzd", type=float, help="Total eligible NZD")
    parser.add_argument("--tokens", type=int, help="Number of tokens")
    parser.add_argument("--fx", type=float, help="FX Rate NZD to AED")
    parser.add_argument("--template", type=str, default="03_studio/templates/investor_report_institutional_lite.html")
    parser.add_argument("--output", type=str, default="03_studio/output/investor_report.html")

    args = parser.parse_args()

    if args.total_eligible_nzd and args.tokens and args.fx:
        data = {
            "total_eligible_nzd": args.total_eligible_nzd,
            "tokens": args.tokens,
            "fx": args.fx
        }
        generate_report(data, args.template, args.output)
    else:
        print("Missing required arguments. Use --help for usage.")
