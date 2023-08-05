// -------------------------------------------------------------------
// Copyright (c) 2013-2017, AIT Austrian Institute of Technology GmbH.
// All rights reserved. See file FMIPP_LICENSE for details.
// -------------------------------------------------------------------

#ifndef _DYNAMICAL_SYSTEM_H
#define _DYNAMICAL_SYSTEM_H

//#include "import/integrators/include/IntegratorProperties.h"
#include "common/fmi_v1.0/fmiModelTypes.h"
#include "import/integrators/include/Integrator.h"


/**
 * \file DynamicalSystem.h
 *
 * \class DynamicalSystem DynamicalSystem.h
 *
 * Reduces FMUs for ME to the functionalities necessary for integration.
 *
 *It also defines which parts
 * of an fmu are actually exposed to the Integrator and IntegratorStepper class. Roughly speaking, these
 * functionalities are
 *
 *   * get/set States
 *   * get/set Time
 *   * check   stateEvents
 *   * check   stepEvents
 *   * get     Derivatives ( righthandside of the ODE )
 *   * get     Jacobian
 *
 * \note
 *          * make sure to keep this class slim since the evaluation speed of these functions
 *            has a tremendous effect on the overall performance of the fmippim module
 *          * Event handling should not be done by this class, but by the derived classes. Giving the continuous
 *            time Integrators access to (discrete time) event handling functions makes no sense.
 */

class __FMI_DLL DynamicalSystem
{
public:

	/// constructor
	DynamicalSystem();

	/// Destructor.
	virtual ~DynamicalSystem();

	/// set the FMU time
	virtual void setTime( fmiTime time ) = 0;

	/// get the FMU time
	virtual fmiReal getTime() const = 0;

	/// get continuous states
	virtual fmiStatus getContinuousStates( fmiReal* x ) = 0;

	/// set continuous states
	virtual fmiStatus setContinuousStates( const fmiReal* x ) = 0;

	/// get the derivatives / righthandside of the ODE
	virtual fmiStatus getDerivatives( fmiReal* dx ) = 0;

	/// get EventIndicators at curret FMU state/time
	virtual fmiStatus getEventIndicators( fmiReal* eventsind ) = 0;

	/// return the number of continuous states
	virtual std::size_t nStates() const = 0;

	/// return the number of event indicators
	virtual std::size_t nEventInds() const = 0;

	/// say wheteher the FMU provides a jacobian ( always false for 1.0 FMUs )
	virtual bool providesJacobian(){ return providesJacobian_; };

	/**
	 * get Jacobian for the current FMU state/time.
	 *
	 * The jacobian gets stored in a vector of length `NEQ`x`NEQ` columnwise, i.e.
	 *
	 *        \f[ J[ NEQ*j + i ]   =    \frac{\partial f_i( x )}{\partial x_j},\ i{,} j = 0,...,NEQ-1 \f]
	 *
	 * \retval fmiOK       The jacobian has been computed without problems
	 * \retval fmiDiscard  at least one call to getDirectionalDerivatives was not sucessfull.
	 *                     The output J should not be used.
	 * \retval fmiWarning  The jacobian is not available because the FMU is of type 1.0 or a flag
	 *                     the model description informs about the missing functionality of
	 *                     fmi2GetDirectionalDerivative.
	 */
	virtual fmiStatus getJac( fmiReal* J );

	/**
	 * calculate the numerical Jacobian
	 *
	 * The result gets stored in a vector of length NEQ*NEQ rowise, i.e.
	 *
	 *        \f[ J[ NEQ*i + j ]   =    \frac{\partial f_i( x )}{\partial x_j},\ i{,} j = 0,...,NEQ-1 \f]
	 *
	 */
	virtual void getNumericalJacobian( fmiReal* J, const fmiReal* x, fmiReal* dfdt, const fmiReal t );

	/// check whether the sign of at least one event indicator changed since the last call
	/// to saveEventIndicators()
	bool checkStateEvent();

	/// call completedIntegratorStep and check for a step event
	virtual bool checkStepEvent() = 0;

	/** Get a struct containig the name and the tolerances of the stepper.
	 *
	 * Use as follows:
	 * \code{.cpp}
	 *     FMUModelExchange fmu( ... );
	 *     // get the tolerance
	 *     fmiReal tolerance = fmu.getIntegratorProperties().tolerance
	 *     // print the name
	 *     std::cout << fmu.getIntegratorProperties().name << std::endl;
	 * \endcode
	 *
	 */
	Integrator::Properties getIntegratorProperties(){
		return integrator_->getProperties();
	}

protected:
	/// Integrator Instance
	Integrator* integrator_;

	/// Flag indicating whether the jacobian can be computed by the fmu
	bool providesJacobian_;

	/// save current event indicators for later calls to checkStateEvent()
	void saveEventIndicators();

private:
	/// Avoid naming conflict with FMUModelExchange::eventsind_
	fmiReal* savedEventIndicators_;

	/// Temporary storage for event indicators.
	fmiReal* currentEventIndicators_;
};

#endif
