class Connect(object):

    def __init__(
        self, username, password="", url="https://sso.apps.xchem.diamond.ac.uk"
    ):
        self.username = username
        self.password = password
        self.url = url
        self.token = None

    def get_token(self):
        """token=$(curl -kL -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=client_credentials' -d 'client_id=squonk-notebook' -d 'client_secret=dpyyjLR2dKUPBw2LfT3Ml3m4GtdeOIU0' https://sso.apps.xchem.diamond.ac.uk/auth/realms/xchem/protocol/openid-connect/token"""
        # TODO Where do we get the client secret from???
        url_extension = "/auth/realms/xchem/protocol/openid-connect/token"
        # Parse response - | grep -Po '(?<="access_token":")[^"]*')"
        token = ""
        self.token = token

    def get_jobs(self):
        """curl -L -H "Authorization: bearer $token" -H "SquonkUsername: user101" http://jobexecutor.squonk.svc:8080"""
        url_extension = "jobexecutor/rest/v1/jobs/"

    def post_job(self):
        """curl -L -H "Authorization: bearer $token" -H "SquonkUsername: user101" http://jobexecutor.squonk.svc:8080"""
        # TODO - quite extensive job preparation needed here - should link to DSD descriptions - and bespoke Python Classes
        url_extension = "jobexecutor/rest/v1/jobs/"

    # These are quite straightforward
    def poll_status(self, job_id):
        """curl -L -H "Authorization: bearer $token" -H "SquonkUsername: user101" http://jobexecutor.squonk.svc:8080/jobexecutor/rest/v1/jobs/<job-id>/status"""
        # Deal here with different options for returned jobs - e.g. RESULTS_READY etc

    def get_results(self, job_id):
        """curl -L -H "Authorization: bearer $token" -H "SquonkUsername: user101" http://jobexecutor.squonk.svc:8080/jobexecutor/rest/v1/jobs/<job-id>/results"""

    def delete_job(self, job_id):
        """curl -L -X DELETE -H "Authorization: bearer $token" -H "SquonkUsername: user101" http://jobexecutor.squonk.svc:8080/jobexecutor/rest/v1/jobs/<job-id>"""
