/*
 * the producer application
 *
 * 
 *
 */


#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>

#include <iostream>
#include <string>
#include <fstream>


using namespace ndn;
using namespace std;


class Producer : noncopyable
{
public:

	void run()
	{
		m_face.setInterestFilter("/ndn-ss",
				bind(&Producer::onInterest, this, _1, _2),
				RegisterPrefixSuccessCallback(),
				bind(&Producer::onRegisterFailed, this, _1, _2));
		
		m_face.processEvents();
	}

private:

	void onInterest(const InterestFilter& filter, const Interest& interest)
	{
		cout << "[*] Recieved interest\n";

		Name n = interest.getName();
		ofstream o_file;
		o_file.open("data.first.txt");

		/* dump the data for the micro service */
		for(auto it = n.begin(); it != n.end(); it++) {
			cout << *it << "\n";
			o_file << *it << "\n";
		}
		o_file.close();

		/* once the data is written, release the semaphore for the sig
		 * ver container */
		o_file.open("sig-ver.sem");
		o_file << 0;
		o_file.close();

		/* wait here for microservice chain to complete
		 */
		// while final.sem == 1 { wait }
		int lock_status = 1;
		ifstream in_file;
		in_file.open("final.sem");

		while(lock_status) {
			in_file.clear();
			in_file.seekg(0,ios::beg);
			in_file >> lock_status;
			sleep(1);
		}

		/* should read in final data here, for now return HELLO
		 */

		Name name(interest.getName());
		name.append("testing").appendVersion();

		char *content = (char*)"HELLO";

		shared_ptr<Data> data = make_shared<Data>();
		data->setName(name);
		data->setFreshnessPeriod(1_s);
		data->setContent(reinterpret_cast<const uint8_t*>(content),strlen(content));

		m_keyChain.sign(*data);
		m_face.put(*data);
	}

	void onRegisterFailed(const Name& prefix, const string& reason)
	{
		cout << "[*] Failed to register prefix: " << reason << "\n";
		m_face.shutdown();
	}


private:
	Face m_face;
	KeyChain m_keyChain;

};



int main(int argc, char *argv[])
{
	cout << "=== starting nfd-entry ===\n";
	Producer producer;

	try {
		producer.run();
	} catch (const std::exception& e) {
		cout << "[!] Error: " << e.what() << "\n";
	}
	return 0;
}